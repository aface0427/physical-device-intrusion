一个支路对应一个断路器和电表
运行函数在main函数中

需要修改：
Config里面branch.json支路配置
在Find in Files中寻找TODO，把未实现的实现

注意：
在新加socket通信函数时，需要加入Config.SocketLock中的socketLock锁,防止多线程读写冲突



