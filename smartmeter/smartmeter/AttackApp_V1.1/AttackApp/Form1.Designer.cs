namespace AttackApp
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
            this.ConnectButton = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.Onbutton1 = new System.Windows.Forms.Button();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.pictureBox2 = new System.Windows.Forms.PictureBox();
            this.Alloffbutton = new System.Windows.Forms.Button();
            this.Allonbutton = new System.Windows.Forms.Button();
            this.Offbutton3 = new System.Windows.Forms.Button();
            this.Onbutton3 = new System.Windows.Forms.Button();
            this.Offbutton2 = new System.Windows.Forms.Button();
            this.Onbutton2 = new System.Windows.Forms.Button();
            this.Offbutton1 = new System.Windows.Forms.Button();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).BeginInit();
            this.SuspendLayout();
            // 
            // ConnectButton
            // 
            this.ConnectButton.BackColor = System.Drawing.Color.Transparent;
            this.ConnectButton.Font = new System.Drawing.Font("宋体", 15F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.ConnectButton.ForeColor = System.Drawing.SystemColors.Desktop;
            this.ConnectButton.Location = new System.Drawing.Point(126, 22);
            this.ConnectButton.Name = "ConnectButton";
            this.ConnectButton.Size = new System.Drawing.Size(278, 40);
            this.ConnectButton.TabIndex = 2;
            this.ConnectButton.Text = "连接";
            this.ConnectButton.UseVisualStyleBackColor = false;
            this.ConnectButton.Click += new System.EventHandler(this.ConnectButton_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.label1.Location = new System.Drawing.Point(19, 99);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(85, 19);
            this.label1.TabIndex = 3;
            this.label1.Text = "第一路：";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.label2.Location = new System.Drawing.Point(19, 156);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(85, 19);
            this.label2.TabIndex = 4;
            this.label2.Text = "第二路：";
            this.label2.Click += new System.EventHandler(this.label2_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.label3.Location = new System.Drawing.Point(19, 214);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(85, 19);
            this.label3.TabIndex = 7;
            this.label3.Text = "第三路：";
            this.label3.Click += new System.EventHandler(this.label3_Click);
            // 
            // Onbutton1
            // 
            this.Onbutton1.Font = new System.Drawing.Font("宋体", 15F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Onbutton1.Location = new System.Drawing.Point(126, 88);
            this.Onbutton1.Name = "Onbutton1";
            this.Onbutton1.Size = new System.Drawing.Size(124, 40);
            this.Onbutton1.TabIndex = 9;
            this.Onbutton1.Text = "断路器合闸";
            this.Onbutton1.UseVisualStyleBackColor = true;
            this.Onbutton1.Click += new System.EventHandler(this.Onbutton1_Click);
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.pictureBox1);
            this.groupBox1.Controls.Add(this.ConnectButton);
            this.groupBox1.Location = new System.Drawing.Point(15, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(434, 75);
            this.groupBox1.TabIndex = 10;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "连接";
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(46, 34);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(16, 16);
            this.pictureBox1.TabIndex = 3;
            this.pictureBox1.TabStop = false;
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.pictureBox2);
            this.groupBox2.Controls.Add(this.Alloffbutton);
            this.groupBox2.Controls.Add(this.Allonbutton);
            this.groupBox2.Controls.Add(this.Offbutton3);
            this.groupBox2.Controls.Add(this.Onbutton3);
            this.groupBox2.Controls.Add(this.Offbutton2);
            this.groupBox2.Controls.Add(this.Onbutton2);
            this.groupBox2.Controls.Add(this.Offbutton1);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.Onbutton1);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.groupBox3);
            this.groupBox2.Location = new System.Drawing.Point(15, 93);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(434, 260);
            this.groupBox2.TabIndex = 11;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "控制";
            this.groupBox2.Enter += new System.EventHandler(this.groupBox2_Enter);
            // 
            // pictureBox2
            // 
            this.pictureBox2.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox2.Image")));
            this.pictureBox2.Location = new System.Drawing.Point(46, 32);
            this.pictureBox2.Name = "pictureBox2";
            this.pictureBox2.Size = new System.Drawing.Size(16, 17);
            this.pictureBox2.TabIndex = 18;
            this.pictureBox2.TabStop = false;
            this.pictureBox2.Click += new System.EventHandler(this.pictureBox2_Click);
            // 
            // Alloffbutton
            // 
            this.Alloffbutton.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Alloffbutton.Location = new System.Drawing.Point(280, 22);
            this.Alloffbutton.Name = "Alloffbutton";
            this.Alloffbutton.Size = new System.Drawing.Size(124, 40);
            this.Alloffbutton.TabIndex = 16;
            this.Alloffbutton.Text = "全跳闸";
            this.Alloffbutton.UseVisualStyleBackColor = true;
            this.Alloffbutton.Click += new System.EventHandler(this.Alloffbutton_Click);
            // 
            // Allonbutton
            // 
            this.Allonbutton.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Allonbutton.Location = new System.Drawing.Point(126, 22);
            this.Allonbutton.Name = "Allonbutton";
            this.Allonbutton.Size = new System.Drawing.Size(124, 40);
            this.Allonbutton.TabIndex = 15;
            this.Allonbutton.Text = "全合闸";
            this.Allonbutton.UseVisualStyleBackColor = true;
            this.Allonbutton.Click += new System.EventHandler(this.Allonbutton_Click);
            // 
            // Offbutton3
            // 
            this.Offbutton3.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Offbutton3.Location = new System.Drawing.Point(280, 205);
            this.Offbutton3.Name = "Offbutton3";
            this.Offbutton3.Size = new System.Drawing.Size(124, 40);
            this.Offbutton3.TabIndex = 14;
            this.Offbutton3.Text = "断路器跳闸";
            this.Offbutton3.UseVisualStyleBackColor = true;
            this.Offbutton3.Click += new System.EventHandler(this.Offbutton3_Click);
            // 
            // Onbutton3
            // 
            this.Onbutton3.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Onbutton3.Location = new System.Drawing.Point(126, 205);
            this.Onbutton3.Name = "Onbutton3";
            this.Onbutton3.Size = new System.Drawing.Size(124, 40);
            this.Onbutton3.TabIndex = 13;
            this.Onbutton3.Text = "断路器合闸";
            this.Onbutton3.UseVisualStyleBackColor = true;
            this.Onbutton3.Click += new System.EventHandler(this.Onbutton3_Click);
            // 
            // Offbutton2
            // 
            this.Offbutton2.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Offbutton2.Location = new System.Drawing.Point(280, 147);
            this.Offbutton2.Name = "Offbutton2";
            this.Offbutton2.Size = new System.Drawing.Size(124, 40);
            this.Offbutton2.TabIndex = 12;
            this.Offbutton2.Text = "断路器跳闸";
            this.Offbutton2.UseVisualStyleBackColor = true;
            this.Offbutton2.Click += new System.EventHandler(this.Offbutton2_Click);
            // 
            // Onbutton2
            // 
            this.Onbutton2.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Onbutton2.Location = new System.Drawing.Point(126, 147);
            this.Onbutton2.Name = "Onbutton2";
            this.Onbutton2.Size = new System.Drawing.Size(124, 40);
            this.Onbutton2.TabIndex = 11;
            this.Onbutton2.Text = "断路器合闸";
            this.Onbutton2.UseVisualStyleBackColor = true;
            this.Onbutton2.Click += new System.EventHandler(this.Onbutton2_Click);
            // 
            // Offbutton1
            // 
            this.Offbutton1.Font = new System.Drawing.Font("宋体", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.Offbutton1.Location = new System.Drawing.Point(280, 88);
            this.Offbutton1.Name = "Offbutton1";
            this.Offbutton1.Size = new System.Drawing.Size(124, 40);
            this.Offbutton1.TabIndex = 10;
            this.Offbutton1.Text = "断路器跳闸";
            this.Offbutton1.UseVisualStyleBackColor = true;
            this.Offbutton1.Click += new System.EventHandler(this.Offbutton1_Click);
            // 
            // groupBox3
            // 
            this.groupBox3.Location = new System.Drawing.Point(7, 70);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(421, 184);
            this.groupBox3.TabIndex = 17;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "手动控制";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 14F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(479, 365);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.Font = new System.Drawing.Font("宋体", 10.5F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.ForeColor = System.Drawing.SystemColors.InfoText;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.Text = "AttackApp";
            this.Load += new System.EventHandler(this.Attack_Load);
            this.groupBox1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox2)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button ConnectButton;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button Onbutton1;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Button Offbutton1;
        private System.Windows.Forms.Button Onbutton2;
        private System.Windows.Forms.Button Offbutton3;
        private System.Windows.Forms.Button Onbutton3;
        private System.Windows.Forms.Button Offbutton2;
        private System.Windows.Forms.Button Alloffbutton;
        private System.Windows.Forms.Button Allonbutton;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.PictureBox pictureBox2;
    }
}

