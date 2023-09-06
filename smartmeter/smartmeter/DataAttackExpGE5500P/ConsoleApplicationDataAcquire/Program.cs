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
        static string version="0.1.7.SH_Attack_edition_GE_5500P";
        static bool RunFlag = true;
        static int SampleCount=0;
        const int SampleTime=10;
        public TCPSGInterface TcpMeter1;
        double Energy1;
        double Energy1new = 9.9;
        double U1, I1, W1;
        uint CT1_1, PT1_1, PT1_2;
        //ushort Pass = 5555; CT=25，PT1=220，PT2=220
        ushort CT1_1new = 25;
        UInt32 PT1_1new = 220;
        ushort PT1_2new = 220;
        UInt32 Energy1new1;
        byte slaveID1 = 7;
        byte[] bholdregs1_1 = new byte[4];
        byte[] bholdregs1_2 = new byte[2];
        byte[] bholdregs1_3 = new byte[2];
        byte[] bholdregs1_4 = new byte[2];
        byte[] bholdregs1_5 = new byte[2];
        byte[] bholdregs1_6 = new byte[4];
        byte[] bholdregs1_7 = new byte[2];
        byte[] bholdregs1_8 = new byte[4];
        byte[] bholdregs1_9 = new byte[2];
        byte[] bholdregs1_10 = new byte[2];
        byte[] bholdregs1_11 = new byte[4];
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
                TcpMeter1 = new TCPSGInterface("192.168.1.108"); 
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
                TcpMeter1.ReadHoldingRegisters(slaveID1, 342, 2, bholdregs1_1);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 309, 1, bholdregs1_2);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 313, 1, bholdregs1_3);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 318, 1, bholdregs1_4);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 264, 1, bholdregs1_5);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 261, 2, bholdregs1_6);
                TcpMeter1.ReadHoldingRegisters(slaveID1, 263, 1, bholdregs1_7);
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
            //Energy1对应电表1的费率1寄存器中的电能
            Array.Reverse(bholdregs1_1, 0, 4);
            Energy1 = BitConverter.ToInt32(bholdregs1_1, 0);
            Array.Reverse(bholdregs1_2, 0, 2);
            U1 = BitConverter.ToUInt16(bholdregs1_2, 0);
            Array.Reverse(bholdregs1_3, 0, 2);
            I1 = BitConverter.ToUInt16(bholdregs1_3, 0);
            Array.Reverse(bholdregs1_4, 0, 2);
            W1 = BitConverter.ToInt16(bholdregs1_4, 0);
            Array.Reverse(bholdregs1_5, 0, 2);
            CT1_1 = BitConverter.ToUInt16(bholdregs1_5, 0);
            Array.Reverse(bholdregs1_6, 0, 4);
            PT1_1 = BitConverter.ToUInt32(bholdregs1_6, 0);
            Array.Reverse(bholdregs1_7, 0, 2);
            PT1_2 = BitConverter.ToUInt16(bholdregs1_7, 0);
            bholdregs1_8 = BitConverter.GetBytes(PT1_1new);
            Array.Reverse(bholdregs1_8, 0, 4);
            bholdregs1_9 = BitConverter.GetBytes(CT1_1new);
            Array.Reverse(bholdregs1_9, 0, 2);
            bholdregs1_10 = BitConverter.GetBytes(PT1_2new);
            Array.Reverse(bholdregs1_10, 0, 2);
            Energy1new1 = Convert.ToUInt32(Energy1new * 10);
            bholdregs1_11 = BitConverter.GetBytes(Energy1new1);
            Array.Reverse(bholdregs1_11, 0, 4);
            

            switch (SampleCount)
            {
                case 0://第一次采样
                    SampleCount++;
                    try
                    {
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 21999, Pass);// in PS update mode
                        //TcpMeter1.WriteMultipleRegistersN(slaveID1, 29999, specil);//change the CT numerator
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 30000, CT1new);
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 30001, PT1new);
                        //TcpMeter1.ReadHoldingRegisters(slaveID1, 22001, 1, bholdregs9);
                        //Array.Reverse(bholdregs9, 0, 2);
                        //checksum = BitConverter.ToUInt16(bholdregs9, 0);
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 22002, checksum);
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 22000, checksum);// out PS update mode
                        TcpMeter1.WriteMultipleRegistersP(slaveID1, 264, bholdregs1_9);
                        TcpMeter1.WriteMultipleRegistersQ(slaveID1, 261, bholdregs1_8);
                        TcpMeter1.WriteMultipleRegistersP(slaveID1, 263, bholdregs1_10);
                        TcpMeter1.WriteMultipleRegistersQ(slaveID1, 342, bholdregs1_11);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("{0}", e.ToString());
                        errorlog.Error(e);
                    }
                    break;
                default:
                    Console.WriteLine("{0}", BitConverter.ToString(bholdregs1_9));
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
            Console.WriteLine("Energy5500P:{0} KWh", (Energy1/10));
            Console.WriteLine("U_5500P:{0} Volts", (U1*(PT1_1/PT1_2)/10));
            Console.WriteLine("I_5500P:{0} Amps", (I1*(CT1_1/5)/1000));
            Console.WriteLine("W_5500P:{0} W", (W1*(PT1_1/PT1_2)*(CT1_1/5)));
            Console.WriteLine("CT_5500P:{0}", CT1_1);
            Console.WriteLine("PT1_5500P:{0}", PT1_1);
            Console.WriteLine("PT2_5500P:{0}", PT1_2);
            Console.WriteLine("{0}", BitConverter.ToString(bholdregs1_8));
            Console.WriteLine("{0}", BitConverter.ToString(bholdregs1_9));
            Console.WriteLine("{0}", BitConverter.ToString(bholdregs1_11));
            CT1_1 = CT1_1new;
            PT1_1 = PT1_1new;
            PT1_2 = PT1_2new;
            //Console.WriteLine("Energy107:{0} Wh", Energy2);
            //Console.WriteLine("Tariff 2 import energy:");
            //Console.WriteLine("Energy106:{0} Wh", Energy3);
            //Console.WriteLine("Energy107:{0} Wh", Energy4);
            //2015.12.26 by sunhong
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
