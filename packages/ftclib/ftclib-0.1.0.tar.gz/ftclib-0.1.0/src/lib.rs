use pyo3::{prelude::*, wrap_pyfunction, Python};

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn rust_sleep(py: Python<'_>) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async  {
        tokio::time::sleep(Duration::from_secs(1)).await;
        Ok(Python::with_gil(|py| py.None()))
    })
}


/// 输入地址、端口、测速地址、线程，即可开始测速，返回测速获取的字节量的一个列表。
#[pyfunction]
#[pyo3(signature = (proxy_host, proxy_port, urls, worker), text_signature = "(proxy_host, b=proxy_port, urls, worker)")]
fn speed_test(py: Python<'_>, proxy_host: String, proxy_port: u32, urls: Vec<String>, worker: i32) -> PyResult<&PyAny> {
    pyo3_asyncio::tokio::future_into_py(py, async move {
        let res = speed(proxy_host.clone(), proxy_port.clone(), urls.clone(), worker).await;
        Ok(Python::with_gil(|py| res.into_py(py)))
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn ftclib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(rust_sleep, m)?)?;
    m.add_function(wrap_pyfunction!(speed_test, m)?)?;
    Ok(())
}

use std::io;
use std::io::Write;
use futures_util::stream::StreamExt;
use std::time::{Duration, Instant};
use reqwest::Proxy;
// use tokio::task::futures;


pub struct SpeedCore{
    pub stopped: bool,
    pub result: Vec<u64>,
    pub break_speed: bool,
    pub started: bool,
    pub no_flush: bool, //不展示测速期间的速度值，这在多线程中尤其重要，不然会有奇怪的bug。

    _interval: u8,
    _count: u64,
    _total_red: u64,
    _delta_red: u64,
    _time_used: Duration,
    _start_time: Instant,
    _statistics_time: Instant,
}




impl SpeedCore{
    pub fn new(interval: Option<u8>, no_flush: Option<bool>) ->SpeedCore{
        SpeedCore{
            _interval: interval.unwrap_or(10),
            stopped: false,
            break_speed: false,
            _start_time: Instant::now(),
            _statistics_time: Instant::now(),
            _total_red: 0,
            _delta_red: 0,
            result: vec![],
            _count: 0,
            _time_used: Duration::from_secs(0),
            started: false,
            no_flush: no_flush.unwrap_or(true),
        }
    }
    async fn record_size(&mut self, received: u64) {
        let cur_time = Instant::now();
        let delta_time = cur_time - self._statistics_time;
        self._time_used = cur_time - self._start_time;
        self._total_red += received;
        if delta_time >= Duration::from_secs(1) {
            // println!("当前时间为: {:?}", cur_time);
            self._statistics_time = cur_time;
            self._show_progress(delta_time.as_secs())
        }
        let a = Duration::from_secs(self._interval as u64);
        if self._time_used > a {
            self.stopped = true;
        }
    }
    fn _show_progress_full(&mut self) {
        let mb_red = self._total_red as f64 / 1024.0 / 1024.0;
        println!("\r[{}> [{:.2} MB/s]", "=".repeat(self._count as usize), mb_red / self._time_used.as_secs_f64());
        io::stdout().flush().unwrap();
        println!("{}", format!("Fetched {:.2} MB in {:.2}s.", mb_red, self._time_used.as_secs_f64()));
    }
    fn _show_progress(&mut self, delta_time: u64){
        let speed: f64 = (self._total_red - self._delta_red) as f64 / delta_time as f64 ;
        let speed_mb: f64 = speed / 1024.0 / 1024.0;
        // self._delta_red = self._total_red
        self._delta_red = self._total_red;
        self._count += 1;
        if !self.no_flush{
            print!("\r[{}> [{:.2} MB/s]", "=".repeat(self._count as usize), speed_mb);
            io::stdout().flush().unwrap();
        }

        if self.result.len() < self._interval as usize {
            self.result.push(speed as u64);
        }
    }
    pub async fn fetch(&mut self, urls: Vec<String>, host: &str, port: u32) {
        // let my_proxy = Proxy::http(format!("http://{}:{}", host, port)).unwrap();
        let url = "socks5://".to_owned() + host + ":" + port.to_string().as_str();
        let my_proxy = Proxy::all(url).unwrap();
        let client = reqwest::Client::builder()
            .danger_accept_invalid_certs(true)
            .proxy(my_proxy)
            .user_agent("FullTClash/4.0")
            .build()
            .unwrap();

        let mut flag = 0;
        // let s1 = std::time::SystemTime::now();
        loop {
            for url in &urls {
                if self.stopped {
                    break;
                }
                let mut stream = client.get(url).timeout(Duration::from_secs((self._interval + 3) as u64))
                    .send()
                    .await
                    .unwrap()
                    .bytes_stream();
                while let Some(item) = stream.next().await {
                    // println!("Chunk: {:?}", item?);
                    if  !self.stopped {
                        if !self.break_speed {
                            match &item {
                                Ok(bytes) => {
                                    // 在Ok分支中可以获取到bytes的值
                                    let len = bytes.len();
                                    if len == 0 {
                                        break;
                                    }
                                    self.record_size(len as u64).await;
                                }
                                Err(err) => {
                                    // 处理错误
                                    println!("error: {:?}", err);
                                    if self._start_time.elapsed() > Duration::from_secs(self._interval as u64){
                                        flag = 1;
                                        self.stopped = true;
                                        break
                                    }
                                }
                            }

                        } else {
                            flag = 1;
                            break;
                        }
                    }else {
                        flag = 1;
                        break
                    }
                }

                if flag == 1 {
                    break;
                }
            }
            if self.stopped || self.break_speed {
                break;
            }
        }
        // self._show_progress_full();
    }
}
pub async fn speed(proxy_host: String, proxy_port: u32, urls: Vec<String>, worker: i32) -> Vec<u64> {
    let mut tasks = Vec::with_capacity(worker as usize);
    let mut res_vec = Vec::with_capacity(worker as usize);
    // let sc = Arc::new(Mutex::new(SpeedCore::new(None)));
    use tokio::spawn;
    for _ in 0..worker {
        let urls = urls.clone();
        let proxy_host = proxy_host.clone();
        let handle = spawn(async move {
            let mut sc1 = SpeedCore::new(None, None);
            sc1.fetch(urls, proxy_host.as_str(), proxy_port).await;
            sc1
        });
        tasks.push(handle);
        // tasks.push(task::spawn(
        //     sc.fetch(urls.clone(), proxy_host, proxy_port)
        // )
        // );
    }
    // println!("{:?}", tasks);
    let mut total = SpeedCore::new(None, None);
    for t in tasks {
        let res = t.await.unwrap();
        total._total_red += res._total_red;
        if res._count > total._count{
            total._count = res._count;
        }
        if res._time_used > total._time_used{
            total._time_used = res._time_used;
        }

        res_vec.push(res.result);

    }
    total._show_progress_full();

    let max_len = res_vec.iter()
        .map(|v| v.len())
        .max()
        .unwrap();

    let new_vec_vec: Vec<Vec<u64>> = res_vec
        .into_iter()
        .map(|mut v| {
            while v.len() < max_len {
                v.push(0);
            }
            v
        })
        .collect();

    let new_vec: Vec<u64> = (0..max_len)
        .map(|i| new_vec_vec.iter().map(|v| v[i]).sum())
        .collect();

    // println!("{:?}", new_vec);
    new_vec
}


#[cfg(test)]
mod tests {
    use super::*;
    #[tokio::test]
    async fn it_works_st(){
        let mut sc = SpeedCore::new(None, Some(true));
        println!("测速即将开始");
        sc.fetch(vec![String::from("https://dl.google.com/dl/android/studio/install/3.4.1.0/android-studio-ide-183.5522156-windows.exe")],
                 "127.0.0.1",
                 11112,
        ).await;
        println!("{:?}", &sc.result);

    }
}
