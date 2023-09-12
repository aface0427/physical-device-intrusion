namespace SmartmeterAttack
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.button8 = new System.Windows.Forms.Button();
            this.button7 = new System.Windows.Forms.Button();
            this.button6 = new System.Windows.Forms.Button();
            this.button5 = new System.Windows.Forms.Button();
            this.实时数据 = new System.Windows.Forms.GroupBox();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.textBox35 = new System.Windows.Forms.TextBox();
            this.textBox34 = new System.Windows.Forms.TextBox();
            this.textBox33 = new System.Windows.Forms.TextBox();
            this.textBox32 = new System.Windows.Forms.TextBox();
            this.textBox31 = new System.Windows.Forms.TextBox();
            this.textBox8 = new System.Windows.Forms.TextBox();
            this.textBox7 = new System.Windows.Forms.TextBox();
            this.textBox6 = new System.Windows.Forms.TextBox();
            this.textBox5 = new System.Windows.Forms.TextBox();
            this.textBox4 = new System.Windows.Forms.TextBox();
            this.p_6 = new System.Windows.Forms.TextBox();
            this.p_5 = new System.Windows.Forms.TextBox();
            this.p_4 = new System.Windows.Forms.TextBox();
            this.p_3 = new System.Windows.Forms.TextBox();
            this.p_2 = new System.Windows.Forms.TextBox();
            this.p_1 = new System.Windows.Forms.TextBox();
            this.c_6 = new System.Windows.Forms.TextBox();
            this.c_5 = new System.Windows.Forms.TextBox();
            this.c_4 = new System.Windows.Forms.TextBox();
            this.c_3 = new System.Windows.Forms.TextBox();
            this.c_2 = new System.Windows.Forms.TextBox();
            this.c_1 = new System.Windows.Forms.TextBox();
            this.textBox16 = new System.Windows.Forms.TextBox();
            this.v_6 = new System.Windows.Forms.TextBox();
            this.v_5 = new System.Windows.Forms.TextBox();
            this.v_4 = new System.Windows.Forms.TextBox();
            this.v_3 = new System.Windows.Forms.TextBox();
            this.v_2 = new System.Windows.Forms.TextBox();
            this.v_1 = new System.Windows.Forms.TextBox();
            this.textBox9 = new System.Windows.Forms.TextBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            this.textBox3 = new System.Windows.Forms.TextBox();
            this.textBox23 = new System.Windows.Forms.TextBox();
            this.操作状态 = new System.Windows.Forms.GroupBox();
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.performanceCounter1 = new System.Diagnostics.PerformanceCounter();
            this.groupBox1.SuspendLayout();
            this.实时数据.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.操作状态.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.performanceCounter1)).BeginInit();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Font = new System.Drawing.Font("宋体", 18F);
            this.button1.Location = new System.Drawing.Point(12, 12);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(260, 38);
            this.button1.TabIndex = 0;
            this.button1.Text = "电表连接";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.Enabled = false;
            this.button2.Font = new System.Drawing.Font("宋体", 18F);
            this.button2.Location = new System.Drawing.Point(6, 26);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(176, 38);
            this.button2.TabIndex = 2;
            this.button2.Text = "攻击 EPM5500P";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // button3
            // 
            this.button3.Enabled = false;
            this.button3.Font = new System.Drawing.Font("宋体", 18F);
            this.button3.Location = new System.Drawing.Point(6, 84);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(176, 38);
            this.button3.TabIndex = 3;
            this.button3.Text = "攻击 PM800";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // button4
            // 
            this.button4.Enabled = false;
            this.button4.Font = new System.Drawing.Font("宋体", 18F);
            this.button4.Location = new System.Drawing.Point(5, 142);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(177, 38);
            this.button4.TabIndex = 4;
            this.button4.Text = "攻击 PAC4200";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // textBox1
            // 
            this.textBox1.Font = new System.Drawing.Font("宋体", 12F);
            this.textBox1.Location = new System.Drawing.Point(100, 100);
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(200, 26);
            this.textBox1.TabIndex = 0;
            this.textBox1.Text = "hahahahahah";
            // 
            // groupBox1
            // 
            this.groupBox1.BackColor = System.Drawing.Color.White;
            this.groupBox1.Controls.Add(this.button8);
            this.groupBox1.Controls.Add(this.button7);
            this.groupBox1.Controls.Add(this.button6);
            this.groupBox1.Controls.Add(this.button2);
            this.groupBox1.Controls.Add(this.button4);
            this.groupBox1.Controls.Add(this.button3);
            this.groupBox1.Font = new System.Drawing.Font("宋体", 13F);
            this.groupBox1.Location = new System.Drawing.Point(12, 56);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(260, 187);
            this.groupBox1.TabIndex = 5;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "攻击演示";
            this.groupBox1.Enter += new System.EventHandler(this.groupBox1_Enter);
            // 
            // button8
            // 
            this.button8.Enabled = false;
            this.button8.Location = new System.Drawing.Point(205, 142);
            this.button8.Name = "button8";
            this.button8.Size = new System.Drawing.Size(44, 38);
            this.button8.TabIndex = 7;
            this.button8.Text = "RST";
            this.button8.UseVisualStyleBackColor = true;
            this.button8.Click += new System.EventHandler(this.button8_Click);
            // 
            // button7
            // 
            this.button7.Enabled = false;
            this.button7.Location = new System.Drawing.Point(205, 84);
            this.button7.Name = "button7";
            this.button7.Size = new System.Drawing.Size(44, 38);
            this.button7.TabIndex = 6;
            this.button7.Text = "RST";
            this.button7.UseVisualStyleBackColor = true;
            this.button7.Click += new System.EventHandler(this.button7_Click);
            // 
            // button6
            // 
            this.button6.BackColor = System.Drawing.Color.White;
            this.button6.Enabled = false;
            this.button6.Location = new System.Drawing.Point(205, 26);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(44, 38);
            this.button6.TabIndex = 5;
            this.button6.Text = "RST";
            this.button6.UseVisualStyleBackColor = true;
            this.button6.Click += new System.EventHandler(this.button6_Click);
            // 
            // button5
            // 
            this.button5.Enabled = false;
            this.button5.Font = new System.Drawing.Font("宋体", 18F);
            this.button5.Location = new System.Drawing.Point(12, 255);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(260, 40);
            this.button5.TabIndex = 6;
            this.button5.Text = "还原";
            this.button5.UseVisualStyleBackColor = true;
            this.button5.Click += new System.EventHandler(this.button5_Click);
            // 
            // 实时数据
            // 
            this.实时数据.Controls.Add(this.tableLayoutPanel1);
            this.实时数据.Font = new System.Drawing.Font("宋体", 13F);
            this.实时数据.Location = new System.Drawing.Point(277, 12);
            this.实时数据.Margin = new System.Windows.Forms.Padding(2);
            this.实时数据.Name = "实时数据";
            this.实时数据.Padding = new System.Windows.Forms.Padding(2);
            this.实时数据.Size = new System.Drawing.Size(462, 255);
            this.实时数据.TabIndex = 7;
            this.实时数据.TabStop = false;
            this.实时数据.Text = "实时数据";
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 7;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 18.56678F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 13.5722F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 13.5722F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 13.5722F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 13.5722F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 13.5722F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 13.5722F));
            this.tableLayoutPanel1.Controls.Add(this.textBox35, 5, 1);
            this.tableLayoutPanel1.Controls.Add(this.textBox34, 4, 1);
            this.tableLayoutPanel1.Controls.Add(this.textBox33, 3, 1);
            this.tableLayoutPanel1.Controls.Add(this.textBox32, 2, 1);
            this.tableLayoutPanel1.Controls.Add(this.textBox31, 1, 1);
            this.tableLayoutPanel1.Controls.Add(this.textBox8, 6, 0);
            this.tableLayoutPanel1.Controls.Add(this.textBox7, 5, 0);
            this.tableLayoutPanel1.Controls.Add(this.textBox6, 4, 0);
            this.tableLayoutPanel1.Controls.Add(this.textBox5, 3, 0);
            this.tableLayoutPanel1.Controls.Add(this.textBox4, 2, 0);
            this.tableLayoutPanel1.Controls.Add(this.p_6, 6, 4);
            this.tableLayoutPanel1.Controls.Add(this.p_5, 5, 4);
            this.tableLayoutPanel1.Controls.Add(this.p_4, 4, 4);
            this.tableLayoutPanel1.Controls.Add(this.p_3, 3, 4);
            this.tableLayoutPanel1.Controls.Add(this.p_2, 2, 4);
            this.tableLayoutPanel1.Controls.Add(this.p_1, 1, 4);
            this.tableLayoutPanel1.Controls.Add(this.c_6, 6, 3);
            this.tableLayoutPanel1.Controls.Add(this.c_5, 5, 3);
            this.tableLayoutPanel1.Controls.Add(this.c_4, 4, 3);
            this.tableLayoutPanel1.Controls.Add(this.c_3, 3, 3);
            this.tableLayoutPanel1.Controls.Add(this.c_2, 2, 3);
            this.tableLayoutPanel1.Controls.Add(this.c_1, 1, 3);
            this.tableLayoutPanel1.Controls.Add(this.textBox16, 0, 3);
            this.tableLayoutPanel1.Controls.Add(this.v_6, 6, 2);
            this.tableLayoutPanel1.Controls.Add(this.v_5, 5, 2);
            this.tableLayoutPanel1.Controls.Add(this.v_4, 4, 2);
            this.tableLayoutPanel1.Controls.Add(this.v_3, 3, 2);
            this.tableLayoutPanel1.Controls.Add(this.v_2, 2, 2);
            this.tableLayoutPanel1.Controls.Add(this.v_1, 1, 2);
            this.tableLayoutPanel1.Controls.Add(this.textBox9, 0, 2);
            this.tableLayoutPanel1.Controls.Add(this.textBox2, 1, 0);
            this.tableLayoutPanel1.Controls.Add(this.textBox3, 0, 4);
            this.tableLayoutPanel1.Controls.Add(this.textBox23, 6, 1);
            this.tableLayoutPanel1.Location = new System.Drawing.Point(5, 44);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 5;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 8.660375F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 8.660375F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 27.55975F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 27.55975F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 27.55975F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(452, 199);
            this.tableLayoutPanel1.TabIndex = 1;
            this.tableLayoutPanel1.Tag = "111";
            this.tableLayoutPanel1.Paint += new System.Windows.Forms.PaintEventHandler(this.tableLayoutPanel1_Paint);
            // 
            // textBox35
            // 
            this.textBox35.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox35.BackColor = System.Drawing.Color.White;
            this.textBox35.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox35.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox35.Font = new System.Drawing.Font("Consolas", 8.5F);
            this.textBox35.Location = new System.Drawing.Point(330, 20);
            this.textBox35.Name = "textBox35";
            this.textBox35.Size = new System.Drawing.Size(55, 14);
            this.textBox35.TabIndex = 41;
            this.textBox35.Text = "PAC4200";
            this.textBox35.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox34
            // 
            this.textBox34.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox34.BackColor = System.Drawing.Color.White;
            this.textBox34.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox34.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox34.Font = new System.Drawing.Font("Consolas", 8.5F);
            this.textBox34.Location = new System.Drawing.Point(269, 20);
            this.textBox34.Name = "textBox34";
            this.textBox34.Size = new System.Drawing.Size(55, 14);
            this.textBox34.TabIndex = 40;
            this.textBox34.Text = "PM800";
            this.textBox34.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox33
            // 
            this.textBox33.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox33.BackColor = System.Drawing.Color.White;
            this.textBox33.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox33.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox33.Font = new System.Drawing.Font("Consolas", 8.5F);
            this.textBox33.Location = new System.Drawing.Point(208, 20);
            this.textBox33.Name = "textBox33";
            this.textBox33.Size = new System.Drawing.Size(55, 14);
            this.textBox33.TabIndex = 39;
            this.textBox33.Text = "PM800";
            this.textBox33.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox32
            // 
            this.textBox32.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox32.BackColor = System.Drawing.Color.White;
            this.textBox32.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox32.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox32.Font = new System.Drawing.Font("Consolas", 8.5F);
            this.textBox32.Location = new System.Drawing.Point(147, 20);
            this.textBox32.Name = "textBox32";
            this.textBox32.Size = new System.Drawing.Size(55, 14);
            this.textBox32.TabIndex = 38;
            this.textBox32.Text = "EPM5500P";
            this.textBox32.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox31
            // 
            this.textBox31.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox31.BackColor = System.Drawing.Color.White;
            this.textBox31.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox31.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox31.Font = new System.Drawing.Font("Consolas", 8.5F);
            this.textBox31.Location = new System.Drawing.Point(86, 20);
            this.textBox31.Name = "textBox31";
            this.textBox31.Size = new System.Drawing.Size(55, 14);
            this.textBox31.TabIndex = 37;
            this.textBox31.Text = "EPM5500P";
            this.textBox31.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox8
            // 
            this.textBox8.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox8.BackColor = System.Drawing.Color.White;
            this.textBox8.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox8.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox8.Font = new System.Drawing.Font("Consolas", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox8.Location = new System.Drawing.Point(391, 3);
            this.textBox8.Name = "textBox8";
            this.textBox8.Size = new System.Drawing.Size(57, 18);
            this.textBox8.TabIndex = 35;
            this.textBox8.Text = "6#";
            this.textBox8.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox7
            // 
            this.textBox7.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox7.BackColor = System.Drawing.Color.White;
            this.textBox7.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox7.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox7.Font = new System.Drawing.Font("Consolas", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox7.Location = new System.Drawing.Point(330, 3);
            this.textBox7.Name = "textBox7";
            this.textBox7.Size = new System.Drawing.Size(55, 18);
            this.textBox7.TabIndex = 34;
            this.textBox7.Text = "5#";
            this.textBox7.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox6
            // 
            this.textBox6.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox6.BackColor = System.Drawing.Color.White;
            this.textBox6.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox6.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox6.Font = new System.Drawing.Font("Consolas", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox6.Location = new System.Drawing.Point(269, 3);
            this.textBox6.Name = "textBox6";
            this.textBox6.Size = new System.Drawing.Size(55, 18);
            this.textBox6.TabIndex = 33;
            this.textBox6.Text = "4#";
            this.textBox6.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox5
            // 
            this.textBox5.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox5.BackColor = System.Drawing.Color.White;
            this.textBox5.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox5.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox5.Font = new System.Drawing.Font("Consolas", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox5.Location = new System.Drawing.Point(208, 3);
            this.textBox5.Name = "textBox5";
            this.textBox5.Size = new System.Drawing.Size(55, 18);
            this.textBox5.TabIndex = 32;
            this.textBox5.Text = "3#";
            this.textBox5.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox4
            // 
            this.textBox4.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox4.BackColor = System.Drawing.Color.White;
            this.textBox4.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox4.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox4.Font = new System.Drawing.Font("Consolas", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox4.Location = new System.Drawing.Point(147, 3);
            this.textBox4.Name = "textBox4";
            this.textBox4.Size = new System.Drawing.Size(55, 18);
            this.textBox4.TabIndex = 31;
            this.textBox4.Text = "2#";
            this.textBox4.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // p_6
            // 
            this.p_6.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.p_6.BackColor = System.Drawing.Color.White;
            this.p_6.Cursor = System.Windows.Forms.Cursors.Default;
            this.p_6.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.p_6.Location = new System.Drawing.Point(391, 158);
            this.p_6.Name = "p_6";
            this.p_6.Size = new System.Drawing.Size(57, 24);
            this.p_6.TabIndex = 28;
            this.p_6.Text = "\r\n";
            this.p_6.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // p_5
            // 
            this.p_5.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.p_5.BackColor = System.Drawing.Color.White;
            this.p_5.Cursor = System.Windows.Forms.Cursors.Default;
            this.p_5.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.p_5.Location = new System.Drawing.Point(330, 158);
            this.p_5.Name = "p_5";
            this.p_5.Size = new System.Drawing.Size(55, 24);
            this.p_5.TabIndex = 27;
            this.p_5.Text = "\r\n";
            this.p_5.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // p_4
            // 
            this.p_4.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.p_4.BackColor = System.Drawing.Color.White;
            this.p_4.Cursor = System.Windows.Forms.Cursors.Default;
            this.p_4.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.p_4.Location = new System.Drawing.Point(269, 158);
            this.p_4.Name = "p_4";
            this.p_4.Size = new System.Drawing.Size(55, 24);
            this.p_4.TabIndex = 26;
            this.p_4.Text = "\r\n";
            this.p_4.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // p_3
            // 
            this.p_3.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.p_3.BackColor = System.Drawing.Color.White;
            this.p_3.Cursor = System.Windows.Forms.Cursors.Default;
            this.p_3.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.p_3.Location = new System.Drawing.Point(208, 158);
            this.p_3.Name = "p_3";
            this.p_3.Size = new System.Drawing.Size(55, 24);
            this.p_3.TabIndex = 25;
            this.p_3.Text = "\r\n";
            this.p_3.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // p_2
            // 
            this.p_2.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.p_2.BackColor = System.Drawing.Color.White;
            this.p_2.Cursor = System.Windows.Forms.Cursors.Default;
            this.p_2.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.p_2.Location = new System.Drawing.Point(147, 158);
            this.p_2.Name = "p_2";
            this.p_2.Size = new System.Drawing.Size(55, 24);
            this.p_2.TabIndex = 24;
            this.p_2.Text = "\r\n";
            this.p_2.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.p_2.TextChanged += new System.EventHandler(this.p_2_TextChanged);
            // 
            // p_1
            // 
            this.p_1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.p_1.BackColor = System.Drawing.Color.White;
            this.p_1.Cursor = System.Windows.Forms.Cursors.Default;
            this.p_1.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.p_1.Location = new System.Drawing.Point(86, 158);
            this.p_1.Name = "p_1";
            this.p_1.Size = new System.Drawing.Size(55, 24);
            this.p_1.TabIndex = 23;
            this.p_1.Text = "\r\n";
            this.p_1.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // c_6
            // 
            this.c_6.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.c_6.BackColor = System.Drawing.Color.White;
            this.c_6.Cursor = System.Windows.Forms.Cursors.Default;
            this.c_6.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.c_6.Location = new System.Drawing.Point(391, 103);
            this.c_6.Name = "c_6";
            this.c_6.Size = new System.Drawing.Size(57, 24);
            this.c_6.TabIndex = 21;
            this.c_6.Text = "\r\n";
            this.c_6.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // c_5
            // 
            this.c_5.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.c_5.BackColor = System.Drawing.Color.White;
            this.c_5.Cursor = System.Windows.Forms.Cursors.Default;
            this.c_5.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.c_5.Location = new System.Drawing.Point(330, 103);
            this.c_5.Name = "c_5";
            this.c_5.Size = new System.Drawing.Size(55, 24);
            this.c_5.TabIndex = 20;
            this.c_5.Text = "\r\n";
            this.c_5.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // c_4
            // 
            this.c_4.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.c_4.BackColor = System.Drawing.Color.White;
            this.c_4.Cursor = System.Windows.Forms.Cursors.Default;
            this.c_4.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.c_4.Location = new System.Drawing.Point(269, 103);
            this.c_4.Name = "c_4";
            this.c_4.Size = new System.Drawing.Size(55, 24);
            this.c_4.TabIndex = 19;
            this.c_4.Text = "\r\n";
            this.c_4.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // c_3
            // 
            this.c_3.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.c_3.BackColor = System.Drawing.Color.White;
            this.c_3.Cursor = System.Windows.Forms.Cursors.Default;
            this.c_3.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.c_3.Location = new System.Drawing.Point(208, 103);
            this.c_3.Name = "c_3";
            this.c_3.Size = new System.Drawing.Size(55, 24);
            this.c_3.TabIndex = 18;
            this.c_3.Text = "\r\n";
            this.c_3.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // c_2
            // 
            this.c_2.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.c_2.BackColor = System.Drawing.Color.White;
            this.c_2.Cursor = System.Windows.Forms.Cursors.Default;
            this.c_2.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.c_2.Location = new System.Drawing.Point(147, 103);
            this.c_2.Name = "c_2";
            this.c_2.Size = new System.Drawing.Size(55, 24);
            this.c_2.TabIndex = 17;
            this.c_2.Text = "\r\n";
            this.c_2.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // c_1
            // 
            this.c_1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.c_1.BackColor = System.Drawing.Color.White;
            this.c_1.Cursor = System.Windows.Forms.Cursors.Default;
            this.c_1.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.c_1.Location = new System.Drawing.Point(86, 103);
            this.c_1.Name = "c_1";
            this.c_1.Size = new System.Drawing.Size(55, 24);
            this.c_1.TabIndex = 16;
            this.c_1.Text = "\r\n";
            this.c_1.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox16
            // 
            this.textBox16.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox16.BackColor = System.Drawing.Color.White;
            this.textBox16.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox16.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox16.Font = new System.Drawing.Font("微软雅黑", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.textBox16.Location = new System.Drawing.Point(21, 105);
            this.textBox16.Name = "textBox16";
            this.textBox16.Size = new System.Drawing.Size(41, 19);
            this.textBox16.TabIndex = 15;
            this.textBox16.Text = "电流";
            this.textBox16.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBox16.TextChanged += new System.EventHandler(this.textBox16_TextChanged);
            // 
            // v_6
            // 
            this.v_6.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.v_6.BackColor = System.Drawing.Color.White;
            this.v_6.Cursor = System.Windows.Forms.Cursors.Default;
            this.v_6.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.v_6.Location = new System.Drawing.Point(391, 49);
            this.v_6.Name = "v_6";
            this.v_6.Size = new System.Drawing.Size(57, 24);
            this.v_6.TabIndex = 14;
            this.v_6.Text = "\r\n";
            this.v_6.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // v_5
            // 
            this.v_5.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.v_5.BackColor = System.Drawing.Color.White;
            this.v_5.Cursor = System.Windows.Forms.Cursors.Default;
            this.v_5.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.v_5.Location = new System.Drawing.Point(330, 49);
            this.v_5.Name = "v_5";
            this.v_5.Size = new System.Drawing.Size(55, 24);
            this.v_5.TabIndex = 13;
            this.v_5.Text = "\r\n";
            this.v_5.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // v_4
            // 
            this.v_4.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.v_4.BackColor = System.Drawing.Color.White;
            this.v_4.Cursor = System.Windows.Forms.Cursors.Default;
            this.v_4.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.v_4.Location = new System.Drawing.Point(269, 49);
            this.v_4.Name = "v_4";
            this.v_4.Size = new System.Drawing.Size(55, 24);
            this.v_4.TabIndex = 12;
            this.v_4.Text = "\r\n";
            this.v_4.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // v_3
            // 
            this.v_3.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.v_3.BackColor = System.Drawing.Color.White;
            this.v_3.Cursor = System.Windows.Forms.Cursors.Default;
            this.v_3.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.v_3.Location = new System.Drawing.Point(208, 49);
            this.v_3.Name = "v_3";
            this.v_3.Size = new System.Drawing.Size(55, 24);
            this.v_3.TabIndex = 11;
            this.v_3.Text = "\r\n";
            this.v_3.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // v_2
            // 
            this.v_2.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.v_2.BackColor = System.Drawing.Color.White;
            this.v_2.Cursor = System.Windows.Forms.Cursors.Default;
            this.v_2.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.v_2.Location = new System.Drawing.Point(147, 49);
            this.v_2.Name = "v_2";
            this.v_2.Size = new System.Drawing.Size(55, 24);
            this.v_2.TabIndex = 10;
            this.v_2.Text = "\r\n";
            this.v_2.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // v_1
            // 
            this.v_1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.v_1.BackColor = System.Drawing.Color.White;
            this.v_1.Cursor = System.Windows.Forms.Cursors.Default;
            this.v_1.Font = new System.Drawing.Font("Consolas", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.v_1.Location = new System.Drawing.Point(86, 49);
            this.v_1.Name = "v_1";
            this.v_1.Size = new System.Drawing.Size(55, 24);
            this.v_1.TabIndex = 9;
            this.v_1.Text = "\r\n";
            this.v_1.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.v_1.TextChanged += new System.EventHandler(this.v_1_TextChanged);
            // 
            // textBox9
            // 
            this.textBox9.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox9.BackColor = System.Drawing.Color.White;
            this.textBox9.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox9.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox9.Font = new System.Drawing.Font("微软雅黑", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.textBox9.Location = new System.Drawing.Point(19, 51);
            this.textBox9.Name = "textBox9";
            this.textBox9.Size = new System.Drawing.Size(44, 19);
            this.textBox9.TabIndex = 8;
            this.textBox9.Text = "电压";
            this.textBox9.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.textBox9.TextChanged += new System.EventHandler(this.textBox9_TextChanged);
            // 
            // textBox2
            // 
            this.textBox2.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox2.BackColor = System.Drawing.Color.White;
            this.textBox2.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox2.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox2.Font = new System.Drawing.Font("Consolas", 11.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.textBox2.Location = new System.Drawing.Point(86, 3);
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(55, 18);
            this.textBox2.TabIndex = 29;
            this.textBox2.Text = "1#";
            this.textBox2.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox3
            // 
            this.textBox3.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox3.BackColor = System.Drawing.Color.White;
            this.textBox3.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox3.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox3.Font = new System.Drawing.Font("微软雅黑", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.textBox3.Location = new System.Drawing.Point(3, 161);
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(77, 19);
            this.textBox3.TabIndex = 43;
            this.textBox3.Text = "有功功率";
            this.textBox3.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // textBox23
            // 
            this.textBox23.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.textBox23.BackColor = System.Drawing.Color.White;
            this.textBox23.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.textBox23.Cursor = System.Windows.Forms.Cursors.Default;
            this.textBox23.Font = new System.Drawing.Font("Consolas", 8.5F);
            this.textBox23.Location = new System.Drawing.Point(392, 20);
            this.textBox23.Name = "textBox23";
            this.textBox23.Size = new System.Drawing.Size(55, 14);
            this.textBox23.TabIndex = 44;
            this.textBox23.Text = "PAC4200";
            this.textBox23.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            // 
            // 操作状态
            // 
            this.操作状态.BackColor = System.Drawing.Color.Transparent;
            this.操作状态.Controls.Add(this.richTextBox1);
            this.操作状态.Font = new System.Drawing.Font("宋体", 13F);
            this.操作状态.Location = new System.Drawing.Point(12, 314);
            this.操作状态.Margin = new System.Windows.Forms.Padding(2);
            this.操作状态.Name = "操作状态";
            this.操作状态.Padding = new System.Windows.Forms.Padding(2);
            this.操作状态.Size = new System.Drawing.Size(740, 92);
            this.操作状态.TabIndex = 8;
            this.操作状态.TabStop = false;
            this.操作状态.Text = "操作状态";
            this.操作状态.Enter += new System.EventHandler(this.groupBox2_Enter_1);
            // 
            // richTextBox1
            // 
            this.richTextBox1.Location = new System.Drawing.Point(5, 21);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.Size = new System.Drawing.Size(733, 68);
            this.richTextBox1.TabIndex = 0;
            this.richTextBox1.Text = "";
            this.richTextBox1.TextChanged += new System.EventHandler(this.richTextBox1_TextChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(765, 411);
            this.Controls.Add(this.操作状态);
            this.Controls.Add(this.实时数据);
            this.Controls.Add(this.button5);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.button1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.Text = "电表攻击演示";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.groupBox1.ResumeLayout(false);
            this.实时数据.ResumeLayout(false);
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.操作状态.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.performanceCounter1)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button button5;
        private System.Windows.Forms.Button button6;
        private System.Windows.Forms.Button button8;
        private System.Windows.Forms.Button button7;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.GroupBox 实时数据;
        private System.Windows.Forms.GroupBox 操作状态;
        private System.Diagnostics.PerformanceCounter performanceCounter1;
        private System.Windows.Forms.RichTextBox richTextBox1;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.TextBox p_6;
        private System.Windows.Forms.TextBox p_5;
        private System.Windows.Forms.TextBox p_4;
        private System.Windows.Forms.TextBox p_3;
        private System.Windows.Forms.TextBox p_2;
        private System.Windows.Forms.TextBox p_1;
        private System.Windows.Forms.TextBox c_6;
        private System.Windows.Forms.TextBox c_5;
        private System.Windows.Forms.TextBox c_4;
        private System.Windows.Forms.TextBox c_3;
        private System.Windows.Forms.TextBox c_2;
        private System.Windows.Forms.TextBox c_1;
        private System.Windows.Forms.TextBox textBox16;
        private System.Windows.Forms.TextBox v_6;
        private System.Windows.Forms.TextBox v_5;
        private System.Windows.Forms.TextBox v_4;
        private System.Windows.Forms.TextBox v_3;
        private System.Windows.Forms.TextBox v_2;
        private System.Windows.Forms.TextBox v_1;
        private System.Windows.Forms.TextBox textBox9;
        private System.Windows.Forms.TextBox textBox35;
        private System.Windows.Forms.TextBox textBox34;
        private System.Windows.Forms.TextBox textBox33;
        private System.Windows.Forms.TextBox textBox32;
        private System.Windows.Forms.TextBox textBox31;
        private System.Windows.Forms.TextBox textBox8;
        private System.Windows.Forms.TextBox textBox7;
        private System.Windows.Forms.TextBox textBox6;
        private System.Windows.Forms.TextBox textBox5;
        private System.Windows.Forms.TextBox textBox4;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.TextBox textBox3;
        private System.Windows.Forms.TextBox textBox23;
    }
}

