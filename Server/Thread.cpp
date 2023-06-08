#include <iostream>
#include <thread>
#include <chrono>

void stopThread(std::thread& thread)
{
    thread.detach();
}

void test()
{
    while (true)
    {
        std::cout << "-------" << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main()
{
    std::thread t(test);
    t.detach();

    std::this_thread::sleep_for(std::chrono::seconds(5));
    std::cout << "main thread sleep finish" << std::endl;
    stopThread(t);

    return 0;
}
