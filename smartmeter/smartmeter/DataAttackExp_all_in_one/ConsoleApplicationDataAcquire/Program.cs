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
        static string version="0.1.8.SH_Attack_edition_All_in_One";
        static bool RunFlag = true;
        static int SampleCount=0;
        const int SampleTime=5;
        public TCPSGInterface TcpMeter7100, TcpMeter6000, TcpMeter7000, TcpMeter42001, TcpMeter42002, TcpMeter42003, TcpMeter_Mgate;   //定义所有表的TCP套接接口名称
        double Energy_total, Energy6000, Energy7000, Energy2200, Energy42001, Energy42002, Energy42003, Energy55001old, Energy55002old, Energy55001, Energy55002;  //定义所有电表的用电量寄存器
        double U_total, I_total, W_total;  //定义总表的电力量测参数
        double U_6000, I_6000, W_6000;     //定义表6000的电力量测参数
        double U_7000, I_7000, W_7000;     //定义表7000的电力量测参数
        double U_2200, I_2200, W_2200;     //定义表2200的电力量测参数
        Single U_42001, I_42001, W_42001;  //定义表4200_1的电力量测参数
        Single U_42002, I_42002, W_42002;  //定义表4200_2的电力量测参数
        Single U_42003, I_42003, W_42003;  //定义表4200_3的电力量测参数
        double U_55001old, I_55001old, W_55001old;  //定义表5500P_1的电力量测参数
        double U_55001, I_55001, W_55001;
        double U_55002old, I_55002old, W_55002old;  //定义表5500P_2的电力量测参数
        double U_55002, I_55002, W_55002; 
        //由于总表并不涉及修改相关寄存器，所以只读取除总表外的电表的该参数，CT代表电流互感比分子，电流互感比分母默认为5，PT1代表电压互感比分子，PT2代表电压互感比分母
        int CT_6000, PT1_6000, PT2_6000;
        int CT_7000, PT1_7000, PT2_7000;
        int CT_2200, PT1_2200, PT2_2200;
        UInt32 CT_42001, PT1_42001, PT2_42001;
        UInt32 CT_42002, PT1_42002, PT2_42002;
        UInt32 CT_42003, PT1_42003, PT2_42003;
        uint CT_55001, PT1_55001, PT2_55001;
        uint CT_55002, PT1_55002, PT2_55002;
        ushort Pass = 5555;               //修改GE电表时需要用到的密码参数，默认是4个5
        //在修改的参数定义时，由于6000/7000/2200只可以修改电压或者电流互感比，故只设置电压电流互感比参数
        ushort CTnew_6000, PT1new_6000, PT2new_6000;
        ushort CTnew_7000, PT1new_7000, PT2new_7000;
        ushort CTnew_2200, PT1new_2200, PT2new_2200;
        UInt32 CTnew_42001, PT1new_42001, PT2new_42001;
        UInt32 CTnew_42002, PT1new_42002, PT2new_42002;
        UInt32 CTnew_42003, PT1new_42003, PT2new_42003;
        ushort CTnew_55001, PT2new_55001; //5500电表的参数寄存器比较奇怪,只能使用如下的参数寄存器设置
        UInt32 PT1new_55001;
        ushort CTnew_55002, PT2new_55002;
        UInt32 PT1new_55002;
        //由于电表4200和5500P可以修改用电量，所以需对其用电量单独设置修改参数
        double Energy55001new, Energy55002new, Energy42001new, Energy42002new, Energy42003new;
        //定义GE电表中的特殊参数，对电表参数修改时需要从电表中读出该参数再写到电表中去
        ushort checksum6000, checksum7000, checksum2200;
        //定义电表通信时使用的Modbus协议的uid号，和PAC4200通信时该参数统一设置成247即可
        byte slaveID7100 = 1;
        byte slaveID6000 = 1;
        byte slaveID7000 = 1;
        byte slaveID2200 = 3;
        byte slaveID55001 = 7;
        byte slaveID55002 = 8;
        byte slaveID4200 = 247;
        //定义存储电表参数的寄存器，总表只需要4个来存储电力参数
        byte[] bholdregs1_1 = new byte[4];  //7100
        byte[] bholdregs1_2 = new byte[4];
        byte[] bholdregs1_3 = new byte[4];
        byte[] bholdregs1_4 = new byte[4];
        byte[] bholdregs2_1 = new byte[4];  //6000
        byte[] bholdregs2_2 = new byte[4];
        byte[] bholdregs2_3 = new byte[4];
        byte[] bholdregs2_4 = new byte[4];
        byte[] bholdregs2_5 = new byte[2];
        byte[] bholdregs2_6 = new byte[2];
        byte[] bholdregs2_7 = new byte[2];
        byte[] bholdregs2_8 = new byte[2];
        byte[] bholdregs2_9 = new byte[2];
        byte[] bholdregs3_1 = new byte[4];  //7000
        byte[] bholdregs3_2 = new byte[4];
        byte[] bholdregs3_3 = new byte[4];
        byte[] bholdregs3_4 = new byte[4];
        byte[] bholdregs3_5 = new byte[2];
        byte[] bholdregs3_6 = new byte[2];
        byte[] bholdregs3_7 = new byte[2];
        byte[] bholdregs3_8 = new byte[2];
        byte[] bholdregs3_9 = new byte[2];
        byte[] bholdregs4_1 = new byte[4];  //2200
        byte[] bholdregs4_2 = new byte[4];
        byte[] bholdregs4_3 = new byte[4];
        byte[] bholdregs4_4 = new byte[4];
        byte[] bholdregs4_5 = new byte[2];
        byte[] bholdregs4_6 = new byte[2];
        byte[] bholdregs4_7 = new byte[2];
        byte[] bholdregs4_8 = new byte[2];
        byte[] bholdregs4_9 = new byte[2];
        byte[] bholdregs5_1 = new byte[8];  //42001
        byte[] bholdregs5_2 = new byte[4];
        byte[] bholdregs5_3 = new byte[4];
        byte[] bholdregs5_4 = new byte[4];
        byte[] bholdregs5_5 = new byte[4];
        byte[] bholdregs5_6 = new byte[4];
        byte[] bholdregs5_7 = new byte[4];
        byte[] bholdregs5_8 = new byte[8];
        byte[] bholdregs5_9 = new byte[4];
        byte[] bholdregs5_10 = new byte[4];
        byte[] bholdregs5_11 = new byte[4];
        byte[] bholdregs6_1 = new byte[8];  //42002
        byte[] bholdregs6_2 = new byte[4];
        byte[] bholdregs6_3 = new byte[4];
        byte[] bholdregs6_4 = new byte[4];
        byte[] bholdregs6_5 = new byte[4];
        byte[] bholdregs6_6 = new byte[4];
        byte[] bholdregs6_7 = new byte[4];
        byte[] bholdregs6_8 = new byte[8];
        byte[] bholdregs6_9 = new byte[4];
        byte[] bholdregs6_10 = new byte[4];
        byte[] bholdregs6_11 = new byte[4];
        byte[] bholdregs7_1 = new byte[8];  //42003
        byte[] bholdregs7_2 = new byte[4];
        byte[] bholdregs7_3 = new byte[4];
        byte[] bholdregs7_4 = new byte[4];
        byte[] bholdregs7_5 = new byte[4];
        byte[] bholdregs7_6 = new byte[4];
        byte[] bholdregs7_7 = new byte[4];
        byte[] bholdregs7_8 = new byte[8];
        byte[] bholdregs7_9 = new byte[4];
        byte[] bholdregs7_10 = new byte[4];
        byte[] bholdregs7_11 = new byte[4];
        byte[] bholdregs8_1 = new byte[4];  //55001
        byte[] bholdregs8_2 = new byte[2];
        byte[] bholdregs8_3 = new byte[2];
        byte[] bholdregs8_4 = new byte[2];
        byte[] bholdregs8_5 = new byte[2];
        byte[] bholdregs8_6 = new byte[4];
        byte[] bholdregs8_7 = new byte[2];
        byte[] bholdregs8_8 = new byte[4];
        byte[] bholdregs8_9 = new byte[2];
        byte[] bholdregs8_10 = new byte[2];
        byte[] bholdregs8_11 = new byte[4];
        byte[] bholdregs9_1 = new byte[4];  //55002
        byte[] bholdregs9_2 = new byte[2];
        byte[] bholdregs9_3 = new byte[2];
        byte[] bholdregs9_4 = new byte[2];
        byte[] bholdregs9_5 = new byte[2];
        byte[] bholdregs9_6 = new byte[4];
        byte[] bholdregs9_7 = new byte[2];
        byte[] bholdregs9_8 = new byte[4];
        byte[] bholdregs9_9 = new byte[2];
        byte[] bholdregs9_10 = new byte[2];
        byte[] bholdregs9_11 = new byte[4];
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
                TcpMeter7100 = new TCPSGInterface("192.168.1.102");
                TcpMeter6000 = new TCPSGInterface("192.168.1.103"); 
                TcpMeter7000 = new TCPSGInterface("192.168.1.104");
                TcpMeter42001 = new TCPSGInterface("192.168.1.105");
                TcpMeter42002 = new TCPSGInterface("192.168.1.106");
                TcpMeter42003 = new TCPSGInterface("192.168.1.107");
                TcpMeter_Mgate = new TCPSGInterface("192.168.1.108");
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
                //read data from meter
                //7100
                TcpMeter7100.ReadHoldingRegisters(slaveID7100, 1499, 2, bholdregs1_1);
                TcpMeter7100.ReadHoldingRegisters(slaveID7100, 999, 2, bholdregs1_2);
                TcpMeter7100.ReadHoldingRegisters(slaveID7100, 1011, 2, bholdregs1_3);
                TcpMeter7100.ReadHoldingRegisters(slaveID7100, 1017, 2, bholdregs1_4);
                //6000
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 1099, 2, bholdregs2_1);
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 999, 2, bholdregs2_2);
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 1011, 2, bholdregs2_3);
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 1017, 2, bholdregs2_4);
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 30000, 1, bholdregs2_5);
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 30001, 1, bholdregs2_6);
                TcpMeter6000.ReadHoldingRegisters(slaveID6000, 30002, 1, bholdregs2_7);
                //7000
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 1499, 2, bholdregs3_1);
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 999, 2, bholdregs3_2);
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 1011, 2, bholdregs3_3);
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 1017, 2, bholdregs3_4);
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 30000, 1, bholdregs3_5);
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 30001, 1, bholdregs3_6);
                TcpMeter7000.ReadHoldingRegisters(slaveID7000, 30002, 1, bholdregs3_7);
                //2200
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 1099, 2, bholdregs4_1);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 999, 2, bholdregs4_2);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 1011, 2, bholdregs4_3);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 1017, 2, bholdregs4_4);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 30000, 1, bholdregs4_5);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 30001, 1, bholdregs4_6);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID2200, 30002, 1, bholdregs4_7);
                //55001
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 342, 2, bholdregs8_1);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 309, 1, bholdregs8_2);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 313, 1, bholdregs8_3);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 318, 1, bholdregs8_4);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 264, 1, bholdregs8_5);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 261, 2, bholdregs8_6);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55001, 263, 1, bholdregs8_7);
                //55002
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 342, 2, bholdregs9_1);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 309, 1, bholdregs9_2);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 313, 1, bholdregs9_3);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 318, 1, bholdregs9_4);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 264, 1, bholdregs9_5);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 261, 2, bholdregs9_6);
                TcpMeter_Mgate.ReadHoldingRegisters(slaveID55002, 263, 1, bholdregs9_7);
                //42001
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 801, 4, bholdregs5_1);
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 1, 2, bholdregs5_2);
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 13, 2, bholdregs5_3);
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 65, 2, bholdregs5_4);
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 50011, 2, bholdregs5_5);
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 50005, 2, bholdregs5_6);
                TcpMeter42001.ReadHoldingRegisters(slaveID4200, 50007, 2, bholdregs5_7);
                //42002
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 801, 4, bholdregs6_1);
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 1, 2, bholdregs6_2);
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 13, 2, bholdregs6_3);
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 65, 2, bholdregs6_4);
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 50011, 2, bholdregs6_5);
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 50005, 2, bholdregs6_6);
                TcpMeter42002.ReadHoldingRegisters(slaveID4200, 50007, 2, bholdregs6_7);
                //42003
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 801, 4, bholdregs7_1);
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 1, 2, bholdregs7_2);
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 13, 2, bholdregs7_3);
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 65, 2, bholdregs7_4);
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 50011, 2, bholdregs7_5);
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 50005, 2, bholdregs7_6);
                TcpMeter42003.ReadHoldingRegisters(slaveID4200, 50007, 2, bholdregs7_7);
            }
            catch (Exception e)
            {
                Console.WriteLine("{0}", e.ToString());
                errorlog.Error(e);
            }
           
            if (System.DateTime.Now.Subtract(dataTime).Seconds > 3)
            {
                Console.WriteLine("too long time between meter reading,drop this data");
                return;
            }
            //协议数据流转换为实际物理数据
            //7100
            Array.Reverse(bholdregs1_1, 0, 4);
            Energy_total = BitConverter.ToInt32(bholdregs1_1, 0);
            Array.Reverse(bholdregs1_2, 0, 4);
            U_total = BitConverter.ToSingle(bholdregs1_2, 0);
            Array.Reverse(bholdregs1_3, 0, 4);
            I_total = BitConverter.ToSingle(bholdregs1_3, 0);
            Array.Reverse(bholdregs1_4, 0, 4);
            W_total = BitConverter.ToSingle(bholdregs1_4, 0);
            //6000
            Array.Reverse(bholdregs2_1, 0, 4);
            Energy6000 = BitConverter.ToInt32(bholdregs2_1, 0);
            Array.Reverse(bholdregs2_2, 0, 4);
            U_6000 = BitConverter.ToSingle(bholdregs2_2, 0);
            Array.Reverse(bholdregs2_3, 0, 4);
            I_6000 = BitConverter.ToSingle(bholdregs2_3, 0);
            Array.Reverse(bholdregs2_4, 0, 4);
            W_6000 = BitConverter.ToSingle(bholdregs2_4, 0);
            Array.Reverse(bholdregs2_5, 0, 2);
            CT_6000 = BitConverter.ToInt16(bholdregs2_5, 0);
            Array.Reverse(bholdregs2_6, 0, 2);
            PT1_6000 = BitConverter.ToInt16(bholdregs2_6, 0);
            Array.Reverse(bholdregs2_7, 0, 2);
            PT2_6000 = BitConverter.ToInt16(bholdregs2_7, 0);
            Energy6000 = Energy6000 / 1000;
            //7000
            Array.Reverse(bholdregs3_1, 0, 4);
            Energy7000 = BitConverter.ToInt32(bholdregs3_1, 0);
            Array.Reverse(bholdregs3_2, 0, 4);
            U_7000 = BitConverter.ToSingle(bholdregs3_2, 0);
            Array.Reverse(bholdregs3_3, 0, 4);
            I_7000 = BitConverter.ToSingle(bholdregs3_3, 0);
            Array.Reverse(bholdregs3_4, 0, 4);
            W_7000 = BitConverter.ToSingle(bholdregs3_4, 0);
            Array.Reverse(bholdregs3_5, 0, 2);
            CT_7000 = BitConverter.ToInt16(bholdregs3_5, 0);
            Array.Reverse(bholdregs3_6, 0, 2);
            PT1_7000 = BitConverter.ToInt16(bholdregs3_6, 0);
            Array.Reverse(bholdregs3_7, 0, 2);
            PT2_7000 = BitConverter.ToInt16(bholdregs3_7, 0);
            Energy7000 = Energy7000 / 1000;
            //2200
            Array.Reverse(bholdregs4_1, 0, 4);
            Energy2200 = BitConverter.ToInt32(bholdregs4_1, 0);
            Array.Reverse(bholdregs4_2, 0, 4);
            U_2200 = BitConverter.ToSingle(bholdregs4_2, 0);
            Array.Reverse(bholdregs4_3, 0, 4);
            I_2200 = BitConverter.ToSingle(bholdregs4_3, 0);
            Array.Reverse(bholdregs4_4, 0, 4);
            W_2200 = BitConverter.ToSingle(bholdregs4_4, 0);
            Array.Reverse(bholdregs4_5, 0, 2);
            CT_2200 = BitConverter.ToInt16(bholdregs4_5, 0);
            Array.Reverse(bholdregs4_6, 0, 2);
            PT1_2200 = BitConverter.ToInt16(bholdregs4_6, 0);
            Array.Reverse(bholdregs4_7, 0, 2);
            PT2_2200 = BitConverter.ToInt16(bholdregs4_7, 0);
            Energy2200 = Energy2200 / 1000;
            //42001
            Array.Reverse(bholdregs5_1, 0, 8);
            Energy42001 = BitConverter.ToDouble(bholdregs5_1, 0);
            Array.Reverse(bholdregs5_2, 0, 4);
            U_42001 = BitConverter.ToSingle(bholdregs5_2, 0);
            Array.Reverse(bholdregs5_3, 0, 4);
            I_42001 = BitConverter.ToSingle(bholdregs5_3, 0);
            Array.Reverse(bholdregs5_4, 0, 4);
            W_42001 = BitConverter.ToSingle(bholdregs5_4, 0);
            Array.Reverse(bholdregs5_5, 0, 4);
            CT_42001 = BitConverter.ToUInt32(bholdregs5_5, 0);
            Array.Reverse(bholdregs5_6, 0, 4);
            PT1_42001 = BitConverter.ToUInt32(bholdregs5_6, 0);
            Array.Reverse(bholdregs5_7, 0, 4);
            PT2_42001 = BitConverter.ToUInt32(bholdregs5_7, 0);
            //42002
            Array.Reverse(bholdregs6_1, 0, 8);
            Energy42002 = BitConverter.ToDouble(bholdregs6_1, 0);
            Array.Reverse(bholdregs6_2, 0, 4);
            U_42002 = BitConverter.ToSingle(bholdregs6_2, 0);
            Array.Reverse(bholdregs6_3, 0, 4);
            I_42002 = BitConverter.ToSingle(bholdregs6_3, 0);
            Array.Reverse(bholdregs6_4, 0, 4);
            W_42002 = BitConverter.ToSingle(bholdregs6_4, 0);
            Array.Reverse(bholdregs6_5, 0, 4);
            CT_42002 = BitConverter.ToUInt32(bholdregs6_5, 0);
            Array.Reverse(bholdregs6_6, 0, 4);
            PT1_42002 = BitConverter.ToUInt32(bholdregs6_6, 0);
            Array.Reverse(bholdregs6_7, 0, 4);
            PT2_42002 = BitConverter.ToUInt32(bholdregs6_7, 0);
            //42003
            Array.Reverse(bholdregs7_1, 0, 8);
            Energy42003 = BitConverter.ToDouble(bholdregs7_1, 0);
            Array.Reverse(bholdregs7_2, 0, 4);
            U_42003 = BitConverter.ToSingle(bholdregs7_2, 0);
            Array.Reverse(bholdregs7_3, 0, 4);
            I_42003 = BitConverter.ToSingle(bholdregs7_3, 0);
            Array.Reverse(bholdregs7_4, 0, 4);
            W_42003 = BitConverter.ToSingle(bholdregs7_4, 0);
            Array.Reverse(bholdregs7_5, 0, 4);
            CT_42003 = BitConverter.ToUInt32(bholdregs7_5, 0);
            Array.Reverse(bholdregs7_6, 0, 4);
            PT1_42003 = BitConverter.ToUInt32(bholdregs7_6, 0);
            Array.Reverse(bholdregs7_7, 0, 4);
            PT2_42003 = BitConverter.ToUInt32(bholdregs7_7, 0);
            //55001
            Array.Reverse(bholdregs8_1, 0, 4);
            Energy55001old = BitConverter.ToInt32(bholdregs8_1, 0);
            Array.Reverse(bholdregs8_2, 0, 2);
            U_55001old = BitConverter.ToUInt16(bholdregs8_2, 0);
            Array.Reverse(bholdregs8_3, 0, 2);
            I_55001old = BitConverter.ToUInt16(bholdregs8_3, 0);
            Array.Reverse(bholdregs8_4, 0, 2);
            W_55001old = BitConverter.ToInt16(bholdregs8_4, 0);
            Array.Reverse(bholdregs8_5, 0, 2);
            CT_55001 = BitConverter.ToUInt16(bholdregs8_5, 0);
            Array.Reverse(bholdregs8_6, 0, 4);
            PT1_55001 = BitConverter.ToUInt32(bholdregs8_6, 0);
            Array.Reverse(bholdregs8_7, 0, 2);
            PT2_55001 = BitConverter.ToUInt16(bholdregs8_7, 0);
            Energy55001 = Energy55001old / 10;
            U_55001 = U_55001old * (PT1_55001 / PT2_55001) / 10;
            I_55001 = I_55001old * (CT_55001 / 5) / 1000;
            W_55001 = W_55001old * (PT1_55001 / PT2_55001) * (CT_55001 / 5);
            //55002
            Array.Reverse(bholdregs9_1, 0, 4);
            Energy55002old = BitConverter.ToInt32(bholdregs9_1, 0);
            Array.Reverse(bholdregs9_2, 0, 2);
            U_55002old = BitConverter.ToUInt16(bholdregs9_2, 0);
            Array.Reverse(bholdregs9_3, 0, 2);
            I_55002old = BitConverter.ToUInt16(bholdregs9_3, 0);
            Array.Reverse(bholdregs9_4, 0, 2);
            W_55002old = BitConverter.ToInt16(bholdregs9_4, 0);
            Array.Reverse(bholdregs9_5, 0, 2);
            CT_55002 = BitConverter.ToUInt16(bholdregs9_5, 0);
            Array.Reverse(bholdregs9_6, 0, 4);
            PT1_55002 = BitConverter.ToUInt32(bholdregs9_6, 0);
            Array.Reverse(bholdregs9_7, 0, 2);
            PT2_55002 = BitConverter.ToUInt16(bholdregs9_7, 0);
            Energy55002 = Energy55002old / 10;
            U_55002 = U_55002old * (PT1_55002 / PT2_55002) / 10;
            I_55002 = I_55002old * (CT_55002 / 5) / 1000;
            W_55002 = W_55002old * (PT1_55002 / PT2_55002) * (CT_55002 / 5);


            switch (SampleCount)
            {
                case 0://第一次采样
                    SampleCount++;
                    try
                    {
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 21001, Pass);// Open Privilieged Command Session
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 21002, Pass);// in PS update mode
                        ////TcpMeter1.WriteMultipleRegistersN(slaveID1, 29999, specil);//change the CT numerator
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 30000, CT2);
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 20001, Pass);//Reset Alarm Log
                        //TcpMeter1.ReadHoldingRegisters(slaveID1, 21003, 1, bholdregs10);//calculate programmable settings checksum
                        //Array.Reverse(bholdregs10, 0, 2);
                        //checksum = BitConverter.ToUInt16(bholdregs10, 0);
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 21004, checksum);//write checksum registers
                        //TcpMeter1.WriteSingleRegisters(slaveID1, 21006, lala);// out PS update mode
                    }
                    catch (Exception e)
                    {
                        Console.WriteLine("{0}", e.ToString());
                        errorlog.Error(e);
                    }
                    break;
                default:
                    //Console.WriteLine("{0}", BitConverter.ToString(bholdregs8));
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
            Console.WriteLine("Energy  Total: {0,8} KWh",Energy_total);
            Console.WriteLine("Energy  Meter1:{0,8}; Meter2:{1,8} KWh", Energy6000, Energy7000);
            Console.WriteLine("Energy  Meter3:{0,8}; Meter4:{1,8} KWh", Energy2200, Energy42001);
            Console.WriteLine("Energy  Meter5:{0,8}; Meter6:{1,8} KWh", Energy42002, Energy42003);
            Console.WriteLine("Energy  Meter7:{0,8}; Meter8:{1,8} KWh", Energy55001, Energy55002);
            Console.WriteLine("U  total: {0,8} Volts", U_total);
            Console.WriteLine("U  Meter1:{0,8}; Meter2:{1,8} Volts", U_6000, U_7000);
            Console.WriteLine("U  Meter3:{0,8}; Meter4:{1,8} Volts", U_2200, U_42001);
            Console.WriteLine("U  Meter5:{0,8}; Meter6:{1,8} Volts", U_42002, U_42003);
            Console.WriteLine("U  Meter7:{0,8}; Meter8:{1,8} Volts", U_55001, U_55002);
            Console.WriteLine("I  total: {0,8} Amps", I_total);
            Console.WriteLine("I  Meter1:{0,8}; Meter2:{1,8} Amps", I_6000, I_7000);
            Console.WriteLine("I  Meter3:{0,8}; Meter4:{1,8} Amps", I_2200, I_42001);
            Console.WriteLine("I  Meter5:{0,8}; Meter6:{1,8} Amps", I_42002, I_42003);
            Console.WriteLine("I  Meter7:{0,8}; Meter8:{1,8} Amps", I_55001, I_55002);
            Console.WriteLine("W  total: {0,8} Watt", W_total);
            Console.WriteLine("W  Meter1:{0,8}; Meter2:{1,8} Watt", W_6000, W_7000);
            Console.WriteLine("W  Meter3:{0,8}; Meter4:{1,8} Watt", W_2200, W_42001);
            Console.WriteLine("W  Meter5:{0,8}; Meter6:{1,8} Watt", W_42002, W_42003);
            Console.WriteLine("W  Meter7:{0,8}; Meter8:{1,8} Watt", W_55001, W_55002);
            Console.WriteLine("CT meter1:{0}; meter2:{1}; meter3:{2}; meter4:{3}", CT_6000, CT_7000, CT_2200, CT_42001);
            Console.WriteLine("CT meter5:{0}; meter6:{1}; meter7:{2}; meter8:{3}", CT_42002, CT_42003, CT_55001, CT_55002);
            Console.WriteLine("PT1 meter1:{0,4}; meter2:{1,4}; meter3:{2,4}; meter4:{3,4}", PT1_6000, PT1_7000, PT1_2200, PT1_42001);
            Console.WriteLine("PT1 meter5:{0,4}; meter6:{1,4}; meter7:{2,4}; meter8:{3,4}", PT1_42002, PT1_42003, PT1_55001, PT1_55002);
            Console.WriteLine("PT2 meter1:{0,4}; meter2:{1,4}; meter3:{2,4}; meter4:{3,4}", PT2_6000, PT2_7000, PT2_2200, PT2_42001);
            Console.WriteLine("PT2 meter5:{0,4}; meter6:{1,4}; meter7:{2,4}; meter8:{3,4}", PT2_42002, PT2_42003, PT2_55001, PT2_55002);
            //2016.3.10 by sunhong
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
                "Energy1:" + Energy_total.ToString() + "Wh ";
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
