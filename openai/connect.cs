using System;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace open
{
    internal class connect
    {
        static void Main(string[] args)
        {
            string filepath = @"E:\softbei\data\data";
            int n = 1;
            int maxTries = 3; // 设置最大尝试次数

            for (int i = 0; i < maxTries; i++)
            {
                try
                {
                    ProcessStartInfo start = new ProcessStartInfo();
                    start.FileName = @"D:\study\Anaconda\install\relate\envs\open\python.exe";
                    start.Arguments = string.Format("{0} \"{1}\" {2}", @"E:\softbei\code\chat.py", filepath, n);

                    start.UseShellExecute = false;
                    start.RedirectStandardOutput = true;

                    Console.WriteLine(start.Arguments);

                    using (Process process = Process.Start(start))
                    {
                        using (StreamReader reader = process.StandardOutput)
                        {
                            string result = reader.ReadToEnd();

                            // 把输出的JSON字符串转换成一个字典
                            Dictionary<string, object> resumeInfo = JsonConvert.DeserializeObject<Dictionary<string, object>>(result);

                            // Find the first occurrence of a left curly brace and remove all characters before it
                            int index = result.IndexOf('{');
                            if (index >= 0)
                            {
                                result = result.Substring(index);
                            }

                            Console.WriteLine(result);

                            // 输出字典中的每一项
                            foreach (KeyValuePair<string, object> item in resumeInfo)
                            {
                                Console.WriteLine($"{item.Key}: {item.Value}");
                            }

                            // 将字典转换为 JSON 字符串并输出
                            string jsonStr = JsonConvert.SerializeObject(resumeInfo);
                            //Console.WriteLine(jsonStr);
                        }
                    }

                    // 如果代码执行到这里，那么表示没有抛出异常，所以可以跳出循环
                    break;
                }
                catch (Exception ex) // 捕获异常
                {
                    // 打印出异常信息
                    Console.WriteLine($"运行出错: {ex.Message}");

                    // 如果已经达到最大尝试次数，则抛出异常
                    if (i == maxTries - 1)
                    {
                        throw;
                    }
                    else
                    {
                        Console.WriteLine("正在尝试重新运行...");
                    }
                }
            }
        }
    }
}
