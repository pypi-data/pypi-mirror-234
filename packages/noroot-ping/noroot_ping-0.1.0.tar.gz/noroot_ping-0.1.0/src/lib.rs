use tokio::net::TcpStream;
use tokio::runtime;
use pyo3::prelude::*;

#[pyfunction]
pub fn ping_tcp(target_ip: String, target_port: i32) -> bool {
    let rt = runtime::Runtime::new().unwrap();
    rt.block_on(aping_tcp(target_ip, target_port))
}

#[pymodule]
fn noroot_ping(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ping_tcp, m)?)?;
    Ok(())
}

async fn aping_tcp(target_ip: String, target_port: i32) -> bool {
    let target = format!("{}:{}", target_ip, target_port);
    TcpStream::connect(target).await.is_ok()
}

#[cfg(test)]
mod tests { 
    use super::*;

    #[test]
    fn test_tcp_ping() {
        let rt = runtime::Runtime::new().unwrap();
        //run python -m http.server
        let result = rt.block_on(aping_tcp(String::from("0.0.0.0"), 8000));
        assert!(result, "ping_tcp failed");
    }
}


