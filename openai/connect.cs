using System;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Collections.Generic;
using Newtonsoft.Json;  // 注意要导入这个包

namespace open
{
    internal class connect
    {
        static void Main(string[] args)
        {
            string resumeText = File.ReadAllText(@"E:\softbei\code\1.txt");
            string systemMessage = File.ReadAllText(@"E:\softbei\code\requirements.txt");

            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = @"D:\study\Anaconda\install\relate\envs\open\python.exe";
            start.Arguments = string.Format("{0} \"{1}\" \"{2}\"", @"E:\softbei\code\chat.py", resumeText, systemMessage);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;

            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();

                    // 把输出的JSON字符串转换成一个字典
                    Dictionary<string, string> resumeInfo = JsonConvert.DeserializeObject<Dictionary<string, string>>(result);

                    // 输出字典中的每一项
                    foreach (KeyValuePair<string, string> item in resumeInfo)
                    {
                        Console.WriteLine($"{item.Key}: {item.Value}");
                    }
                }
            }
        }
    }
}
