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
            string filepath = @"E:\softbei\code";
            int n = 3;

            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = @"D:\study\Anaconda\install\relate\envs\open\python.exe";
            start.Arguments = string.Format("{0} \"{1}\" {2}", @"E:\softbei\code\chat.py", filepath, n);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;

            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    //Console.WriteLine(result);

                    // 把输出的JSON字符串转换成一个字典
                    Dictionary<string, object> resumeInfo = JsonConvert.DeserializeObject<Dictionary<string, object>>(result);

                    // 输出字典中的每一项
                    foreach (KeyValuePair<string, object> item in resumeInfo)
                    {
                        Console.WriteLine($"{item.Key}: {item.Value}");
                    }

                    // 将字典转换为 JSON 字符串并输出
                    string jsonStr = JsonConvert.SerializeObject(resumeInfo);
                    Console.WriteLine(jsonStr);
                }
            }
        }
    }
}
