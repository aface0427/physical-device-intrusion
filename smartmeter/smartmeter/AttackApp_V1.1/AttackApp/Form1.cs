using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
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

namespace AttackApp
{
    public partial class Form1 : Form
    {
        const int SampleTime1 = 1;
        const int SampleTime2 = 1;
        public TCPSGInterface TcpMeter1;
        bool sfereon = true;
        bool bIsOpen = false;
        byte slaveID1 = 84;
        byte slaveID2 = 86;
        byte slaveID3 = 87;
     
        public Form1()
        {
            InitializeComponent();
        }

        
        private void Attack_Load(object sender, EventArgs e)
        {

        }

        private void ConnectButton_Click(object sender, EventArgs e)
        {
            Console.WriteLine("press connect button");
            if (bIsOpen == false)//disconnect--->connect
            {
                try
                {
                    TcpMeter1 = new TCPSGInterface("192.168.1.90");
                    bIsOpen = true;
                    Allonbutton.Enabled = true;
                    Alloffbutton.Enabled = true;
                    Onbutton1.Enabled = true;
                    Offbutton1.Enabled = true;
                    Onbutton2.Enabled = true;
                    Offbutton2.Enabled = true;
                    Onbutton3.Enabled = true;
                    Offbutton3.Enabled = true;
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
                    Allonbutton.Enabled = false;
                    Alloffbutton.Enabled = false;
                    Onbutton1.Enabled = false;
                    Offbutton1.Enabled = false;
                    Onbutton2.Enabled = false;
                    Offbutton2.Enabled = false;
                    Onbutton3.Enabled = false;
                    Offbutton3.Enabled = false;
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.ToString());
                }
            }

            ConnectButton.Text = bIsOpen ? "断开" : "连接";
            if (bIsOpen) pictureBox1.Image = Properties.Resources.MISC15;
            else pictureBox1.Image = Properties.Resources.MISC14;
        }

        private void Allonbutton_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID1, 1, sfereon);
            TcpMeter1.WriteSingleCoil(slaveID2, 1, sfereon);
            TcpMeter1.WriteSingleCoil(slaveID3, 1, sfereon);
            pictureBox2.Image = Properties.Resources.MISC15;
        }

        private void Alloffbutton_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID1, 2, sfereon);
            TcpMeter1.WriteSingleCoil(slaveID2, 2, sfereon);
            TcpMeter1.WriteSingleCoil(slaveID3, 2, sfereon);
            pictureBox2.Image = Properties.Resources.MISC14;
        }

        private void Onbutton1_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID1, 1, sfereon);
        }


        private void Offbutton1_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID1, 2, sfereon);
        }


        private void Onbutton2_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID2, 1, sfereon);
        }

        private void Offbutton2_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID2, 2, sfereon);
        }

        private void Onbutton3_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID3, 1, sfereon);
        }

        private void Offbutton3_Click(object sender, EventArgs e)
        {
            TcpMeter1.WriteSingleCoil(slaveID3, 2, sfereon);
        }

        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {

        }
    }
}
