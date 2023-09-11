using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MeterInterface;
using System.Threading;
using System.Data;
using System.Data.SqlClient;
using System.Timers;
using log4net;
using log4net.Config;
using System.IO;


namespace ConsoleApplicationDataAcquire
{
    class Program
    {
        static string version="0.1.7.SH_Attack_edition_GE_6000";
        static bool RunFlag = true;
        static int SampleCount=0;
        const int SampleTime=10;
        public TCPSGInterface TcpMeter1;
        double Energy1;
        double U1, I1, W1;
        int CT1, PT1, PT2;
        ushort Pass = 5555;
        // CT=25,PT1=120,PT2=120
        ushort CT1new = 25;
        ushort PT1new = 240;
        ushort checksum;
        byte slaveID1 = 1;
        byte[] bholdregs1 = new byte[4];
        byte[] bholdregs2 = new byte[4];
        byte[] bholdregs3 = new byte[4];
        byte[] bholdregs4 = new byte[4];
        byte[] bholdregs5 = new byte[2];
        byte[] bholdregs6 = new byte[2];
        byte[] bholdregs7 = new byte[2];
        byte[] bholdregs8 = new byte[2];
        byte[] bholdregs9 = new byte[2];
        //byte[] specil = { (byte)0x05,(byte)0x01,(byte)0x00,(byte)0x32,(byte)0x00,(byte)0x78,(byte)0x00,(byte)0x78,(byte)0x01,(byte)0x00,(byte)0x0f,(byte)0x01,(byte)0x03,(byte)0x01,(byte)0x00,(byte)0xff};
        //时间，用于记录读取数据的时间
        DateTime dataTime;
        bool error=false;
        System.Timers.Timer aTimer;
        //log configuration in app.config 日志组件
        log4net.ILog datalog = log4net.LogManager.GetLogger("DataLogger");
        log4net.ILog errorlog = log4net.LogManager.GetLogger("ErrorLogger");

        //检测程序是否停止
        public void DetectStopFunc()
        {
            Console.ReadKey(true);
            RunFlag = !RunFlag;
            //aTimer.Enabled = RunFlag;
            if(!RunFlag)
                Console.WriteLine("Process stopped.Press any key to continue");
            else
                Console.WriteLine("Process started.Press any key to stop");
        }

        Program()
        {
            try
            {
                //电表连接
                TcpMeter1 = new TCPSGInterface("192.168.1.103"); 
            }
            catch (Exception e)
            {
                error = true;
                Console.WriteLine("{0}", e.ToString());
                errorlog.Error(e);
            }

        }
        void Data2mssql()
        {
            if (error)
            {
                Console.WriteLine("Something error happened");
                return;
            }
            dataTime = System.DateTime.Now;
            try
            {
                //meter6000_103,read data from meter
                TcpMeter1.ReadHoldingRegisters(slaveID1, 1099, 2, bholdregs1);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 999, 2, bholdregs2);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 1011, 2, bholdregs3);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 1017, 2, bholdregs4);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 30000, 1, bholdregs5);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 30001, 1, bholdregs6);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 30002, 1, bholdregs7);
            }
            catch (Exception e)
            {
                Console.WriteLine("{0}", e.ToString());
                errorlog.Error(e);
            }
           
            if (System.DateTime.Now.Subtract(dataTime).Seconds > 1)
            {
                Console.WriteLine("too long time between meter reading,drop this data");
                return;
            }
            //协议数据流转换为实际物理数据
            //Energy1对应电表1的寄存器中的电能
            Array.Reverse(bholdregs1, 0, 4);
            Energy1 = BitConverter.ToInt32(bholdregs1, 0);
            Array.Reverse(bholdregs2, 0, 4);
            U1 = BitConverter.ToSingle(bholdregs2, 0);
            Array.Reverse(bholdregs3, 0, 4);
            I1 = BitConverter.ToSingle(bholdregs3, 0);
            Array.Reverse(bholdregs4, 0, 4);
            W1 = BitConverter.ToSingle(bholdregs4, 0);
            Array.Reverse(bholdregs5, 0, 2);
            CT1 = BitConverter.ToInt16(bholdregs5, 0);
            Array.Reverse(bholdregs6, 0, 2);
            PT1 = BitConverter.ToInt16(bholdregs6, 0);
            Array.Reverse(bholdregs7, 0, 2);
            PT2 = BitConverter.ToInt16(bholdregs7, 0);
            bholdregs8 = BitConverter.GetBytes(Pass);
            Array.Reverse(bholdregs8, 0, 2);
            //bholdregs9 = BitConverter.GetBytes(CT2);
            //Array.Reverse(bholdregs9, 0, 2);
            //specil[2] = bholdregs9[0];
            //specil[3] = bholdregs9[1];
            //bholdregs11 = BitConverter.GetBytes(PT1new);
            //Array.Reverse(bholdregs11, 0, 2);
            //specil[4] = bholdregs11[0];
            //specil[5] = bholdregs11[1];

            switch (SampleCount)
            {
                case 0://第一次采样
                    SampleCount++;
                    try
                    {
                        TcpMeter1.WriteSingleRegisters(slaveID1, 21999, Pass);// in PS update mode
                        //TcpMeter1.WriteMultipleRegistersN(slaveID1, 29999, specil);//change the CT numerator
                        TcpMeter1.WriteSingleRegisters(slaveID1, 30000, CT1new);
                        TcpMeter1.WriteSingleRegisters(slaveID1, 30001, PT1new);
                        TcpMeter1.ReadHoldingRegisters(slaveID1, 22001, 1, bholdregs9);
                        Array.Reverse(bholdregs9, 0, 2);
                        checksum= BitConverter.ToUInt16(bholdregs9, 0);
                        TcpMeter1.WriteSingleRegisters(slaveID1, 22002, checksum);
                        TcpMeter1.WriteSingleRegisters(slaveID1, 22000, checksum);// out PS update mode
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("{0}", e.ToString());
                        errorlog.Error(e);
                    }
                    break;
                default:
                    Console.WriteLine("{0}", BitConverter.ToString(bholdregs8));
                    break;


            }
            LogInfo();
            DebugInfo();
        }



        /// <summary>
        /// 调试用
        /// </summary>
        void DebugInfo()
        {
            Console.WriteLine("**************************************");
            Console.WriteLine("{0}", dataTime);
            //Console.WriteLine("Tariff 1 import energy:");
            Console.WriteLine("Energy103:{0} KWh", (Energy1/1000));
            Console.WriteLine("U_103:{0} Volts", U1);
            Console.WriteLine("I_103:{0} Amps", I1);
            Console.WriteLine("W_103:{0} Watt", W1); 
            Console.WriteLine("CT_103:{0}", CT1);
            Console.WriteLine("PT1_103:{0}", PT1); 
            Console.WriteLine("PT2_103:{0}", PT2);
            Console.WriteLine("{0}", BitConverter.ToString(bholdregs1));
            Console.WriteLine("{0}", BitConverter.ToString(bholdregs8));
            Console.WriteLine("{0}", BitConverter.ToString(bholdregs9));
            //Console.WriteLine("{0}", BitConverter.ToString(specil));
            //2016.3.6 by sunhong
            Console.WriteLine("**************************************");
        }

        /// <summary>
        /// using log4net, write log to [logfile]
        /// configuration in:AssemblyInfo.cs &amp; app.config
        /// </summary>
        void LogInfo()
        {
            string LogStr;
            LogStr =
                "Date:"+dataTime.ToString()+" "+
                "Energy1:" + Energy1.ToString() + "Wh ";
            datalog.Info(LogStr);
        }

        /// <summary>
        /// 程序入口
        /// </summary>
        /// <param name="args"></param>
        static void Main(string[] args)
        {
            Console.WriteLine("SmartMemte DataAcquire Program");
            Console.WriteLine("Version:{0}",version);
            Console.WriteLine("SampleTime: {0} seconds",SampleTime);
            Console.WriteLine("waiting......");
            Program a = new Program();
            Thread aThread = new Thread(new ThreadStart(a.DetectStopFunc));
            aThread.Start();
            Console.WriteLine("<Start>");
            while (RunFlag)
            {
                a.Data2mssql();
                System.Threading.Thread.Sleep(SampleTime*1000);
                //a.DetectStopFunc();
            }

            Console.ReadKey(true);
        }


    }
}
