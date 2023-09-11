<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        If disposing AndAlso components IsNot Nothing Then
            components.Dispose()
        End If
        MyBase.Dispose(disposing)
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container
        Me.btnOpen = New System.Windows.Forms.Button
        Me.btnClose = New System.Windows.Forms.Button
        Me.Label1 = New System.Windows.Forms.Label
        Me.cmbcom = New System.Windows.Forms.ComboBox
        Me.Label2 = New System.Windows.Forms.Label
        Me.cmbbaud = New System.Windows.Forms.ComboBox
        Me.Label3 = New System.Windows.Forms.Label
        Me.cmbdb = New System.Windows.Forms.ComboBox
        Me.Label4 = New System.Windows.Forms.Label
        Me.cmbpty = New System.Windows.Forms.ComboBox
        Me.Label5 = New System.Windows.Forms.Label
        Me.cmbsb = New System.Windows.Forms.ComboBox
        Me.Label6 = New System.Windows.Forms.Label
        Me.Label7 = New System.Windows.Forms.Label
        Me.Label8 = New System.Windows.Forms.Label
        Me.Label9 = New System.Windows.Forms.Label
        Me.AI0 = New System.Windows.Forms.TextBox
        Me.AI1 = New System.Windows.Forms.TextBox
        Me.AI2 = New System.Windows.Forms.TextBox
        Me.AI3 = New System.Windows.Forms.TextBox
        Me.AO0 = New System.Windows.Forms.TextBox
        Me.AO1 = New System.Windows.Forms.TextBox
        Me.AO2 = New System.Windows.Forms.TextBox
        Me.AO3 = New System.Windows.Forms.TextBox
        Me.DI0 = New System.Windows.Forms.PictureBox
        Me.DI1 = New System.Windows.Forms.PictureBox
        Me.DI2 = New System.Windows.Forms.PictureBox
        Me.DI3 = New System.Windows.Forms.PictureBox
        Me.DO0 = New System.Windows.Forms.PictureBox
        Me.DO1 = New System.Windows.Forms.PictureBox
        Me.DO2 = New System.Windows.Forms.PictureBox
        Me.DO3 = New System.Windows.Forms.PictureBox
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        CType(Me.DI0, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DI1, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DI2, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DI3, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DO0, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DO1, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DO2, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.DO3, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'btnOpen
        '
        Me.btnOpen.Location = New System.Drawing.Point(657, 69)
        Me.btnOpen.Margin = New System.Windows.Forms.Padding(4, 5, 4, 5)
        Me.btnOpen.Name = "btnOpen"
        Me.btnOpen.Size = New System.Drawing.Size(143, 45)
        Me.btnOpen.TabIndex = 0
        Me.btnOpen.Text = "Open COM"
        Me.btnOpen.UseVisualStyleBackColor = True
        '
        'btnClose
        '
        Me.btnClose.Location = New System.Drawing.Point(657, 131)
        Me.btnClose.Margin = New System.Windows.Forms.Padding(3, 4, 3, 4)
        Me.btnClose.Name = "btnClose"
        Me.btnClose.Size = New System.Drawing.Size(143, 45)
        Me.btnClose.TabIndex = 1
        Me.btnClose.Text = "Close COM"
        Me.btnClose.UseVisualStyleBackColor = True
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(12, 28)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(45, 19)
        Me.Label1.TabIndex = 2
        Me.Label1.Text = "Com"
        '
        'cmbcom
        '
        Me.cmbcom.FormattingEnabled = True
        Me.cmbcom.Items.AddRange(New Object() {"COM1", "COM2", "COM3", "COM4"})
        Me.cmbcom.Location = New System.Drawing.Point(63, 23)
        Me.cmbcom.Name = "cmbcom"
        Me.cmbcom.Size = New System.Drawing.Size(78, 27)
        Me.cmbcom.TabIndex = 3
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(160, 28)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(55, 19)
        Me.Label2.TabIndex = 4
        Me.Label2.Text = "Baud."
        '
        'cmbbaud
        '
        Me.cmbbaud.FormattingEnabled = True
        Me.cmbbaud.Items.AddRange(New Object() {"115200", "9600"})
        Me.cmbbaud.Location = New System.Drawing.Point(221, 25)
        Me.cmbbaud.Name = "cmbbaud"
        Me.cmbbaud.Size = New System.Drawing.Size(97, 27)
        Me.cmbbaud.TabIndex = 5
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(338, 28)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(76, 19)
        Me.Label3.TabIndex = 6
        Me.Label3.Text = "Data Bit"
        '
        'cmbdb
        '
        Me.cmbdb.FormattingEnabled = True
        Me.cmbdb.Items.AddRange(New Object() {"8", "7", "6", "5", "4"})
        Me.cmbdb.Location = New System.Drawing.Point(420, 23)
        Me.cmbdb.Name = "cmbdb"
        Me.cmbdb.Size = New System.Drawing.Size(73, 27)
        Me.cmbdb.TabIndex = 7
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.Location = New System.Drawing.Point(504, 28)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(58, 19)
        Me.Label4.TabIndex = 8
        Me.Label4.Text = "Parity"
        '
        'cmbpty
        '
        Me.cmbpty.FormattingEnabled = True
        Me.cmbpty.Items.AddRange(New Object() {"None", "Even", "Odd"})
        Me.cmbpty.Location = New System.Drawing.Point(568, 23)
        Me.cmbpty.Name = "cmbpty"
        Me.cmbpty.Size = New System.Drawing.Size(83, 27)
        Me.cmbpty.TabIndex = 9
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(667, 28)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(74, 19)
        Me.Label5.TabIndex = 10
        Me.Label5.Text = "Stop Bit"
        '
        'cmbsb
        '
        Me.cmbsb.FormattingEnabled = True
        Me.cmbsb.Items.AddRange(New Object() {"1", "2"})
        Me.cmbsb.Location = New System.Drawing.Point(747, 25)
        Me.cmbsb.Name = "cmbsb"
        Me.cmbsb.Size = New System.Drawing.Size(53, 27)
        Me.cmbsb.TabIndex = 11
        '
        'Label6
        '
        Me.Label6.AutoSize = True
        Me.Label6.Location = New System.Drawing.Point(12, 224)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(28, 19)
        Me.Label6.TabIndex = 12
        Me.Label6.Text = "AI"
        '
        'Label7
        '
        Me.Label7.AutoSize = True
        Me.Label7.Location = New System.Drawing.Point(12, 276)
        Me.Label7.Name = "Label7"
        Me.Label7.Size = New System.Drawing.Size(33, 19)
        Me.Label7.TabIndex = 13
        Me.Label7.Text = "AO"
        '
        'Label8
        '
        Me.Label8.AutoSize = True
        Me.Label8.Location = New System.Drawing.Point(12, 95)
        Me.Label8.Name = "Label8"
        Me.Label8.Size = New System.Drawing.Size(28, 19)
        Me.Label8.TabIndex = 14
        Me.Label8.Text = "DI"
        '
        'Label9
        '
        Me.Label9.AutoSize = True
        Me.Label9.Location = New System.Drawing.Point(12, 167)
        Me.Label9.Name = "Label9"
        Me.Label9.Size = New System.Drawing.Size(33, 19)
        Me.Label9.TabIndex = 15
        Me.Label9.Text = "DO"
        '
        'AI0
        '
        Me.AI0.Location = New System.Drawing.Point(63, 221)
        Me.AI0.Name = "AI0"
        Me.AI0.Size = New System.Drawing.Size(100, 27)
        Me.AI0.TabIndex = 16
        Me.AI0.Tag = ""
        '
        'AI1
        '
        Me.AI1.Location = New System.Drawing.Point(181, 221)
        Me.AI1.Name = "AI1"
        Me.AI1.Size = New System.Drawing.Size(100, 27)
        Me.AI1.TabIndex = 17
        Me.AI1.Tag = ""
        '
        'AI2
        '
        Me.AI2.Location = New System.Drawing.Point(300, 221)
        Me.AI2.Name = "AI2"
        Me.AI2.Size = New System.Drawing.Size(100, 27)
        Me.AI2.TabIndex = 18
        Me.AI2.Tag = ""
        '
        'AI3
        '
        Me.AI3.Location = New System.Drawing.Point(420, 218)
        Me.AI3.Name = "AI3"
        Me.AI3.Size = New System.Drawing.Size(100, 27)
        Me.AI3.TabIndex = 19
        Me.AI3.Tag = ""
        '
        'AO0
        '
        Me.AO0.Location = New System.Drawing.Point(63, 273)
        Me.AO0.Name = "AO0"
        Me.AO0.Size = New System.Drawing.Size(100, 27)
        Me.AO0.TabIndex = 20
        Me.AO0.Tag = "0"
        '
        'AO1
        '
        Me.AO1.Location = New System.Drawing.Point(181, 273)
        Me.AO1.Name = "AO1"
        Me.AO1.Size = New System.Drawing.Size(100, 27)
        Me.AO1.TabIndex = 21
        Me.AO1.Tag = "1"
        '
        'AO2
        '
        Me.AO2.Location = New System.Drawing.Point(300, 273)
        Me.AO2.Name = "AO2"
        Me.AO2.Size = New System.Drawing.Size(100, 27)
        Me.AO2.TabIndex = 22
        Me.AO2.Tag = "2"
        '
        'AO3
        '
        Me.AO3.Location = New System.Drawing.Point(420, 273)
        Me.AO3.Name = "AO3"
        Me.AO3.Size = New System.Drawing.Size(100, 27)
        Me.AO3.TabIndex = 23
        Me.AO3.Tag = "3"
        '
        'DI0
        '
        Me.DI0.BackColor = System.Drawing.Color.Navy
        Me.DI0.Location = New System.Drawing.Point(63, 81)
        Me.DI0.Name = "DI0"
        Me.DI0.Size = New System.Drawing.Size(60, 50)
        Me.DI0.TabIndex = 24
        Me.DI0.TabStop = False
        Me.DI0.Tag = ""
        '
        'DI1
        '
        Me.DI1.BackColor = System.Drawing.Color.Navy
        Me.DI1.Location = New System.Drawing.Point(147, 81)
        Me.DI1.Name = "DI1"
        Me.DI1.Size = New System.Drawing.Size(60, 50)
        Me.DI1.TabIndex = 25
        Me.DI1.TabStop = False
        Me.DI1.Tag = ""
        '
        'DI2
        '
        Me.DI2.BackColor = System.Drawing.Color.Navy
        Me.DI2.Location = New System.Drawing.Point(233, 81)
        Me.DI2.Name = "DI2"
        Me.DI2.Size = New System.Drawing.Size(60, 50)
        Me.DI2.TabIndex = 26
        Me.DI2.TabStop = False
        Me.DI2.Tag = ""
        '
        'DI3
        '
        Me.DI3.BackColor = System.Drawing.Color.Navy
        Me.DI3.Location = New System.Drawing.Point(321, 81)
        Me.DI3.Name = "DI3"
        Me.DI3.Size = New System.Drawing.Size(60, 50)
        Me.DI3.TabIndex = 27
        Me.DI3.TabStop = False
        Me.DI3.Tag = ""
        '
        'DO0
        '
        Me.DO0.BackColor = System.Drawing.Color.DarkRed
        Me.DO0.Location = New System.Drawing.Point(63, 148)
        Me.DO0.Name = "DO0"
        Me.DO0.Size = New System.Drawing.Size(60, 50)
        Me.DO0.TabIndex = 28
        Me.DO0.TabStop = False
        Me.DO0.Tag = "0"
        '
        'DO1
        '
        Me.DO1.BackColor = System.Drawing.Color.DarkRed
        Me.DO1.Location = New System.Drawing.Point(147, 148)
        Me.DO1.Name = "DO1"
        Me.DO1.Size = New System.Drawing.Size(60, 50)
        Me.DO1.TabIndex = 29
        Me.DO1.TabStop = False
        Me.DO1.Tag = "1"
        '
        'DO2
        '
        Me.DO2.BackColor = System.Drawing.Color.DarkRed
        Me.DO2.Location = New System.Drawing.Point(233, 148)
        Me.DO2.Name = "DO2"
        Me.DO2.Size = New System.Drawing.Size(60, 50)
        Me.DO2.TabIndex = 30
        Me.DO2.TabStop = False
        Me.DO2.Tag = "2"
        '
        'DO3
        '
        Me.DO3.BackColor = System.Drawing.Color.DarkRed
        Me.DO3.Location = New System.Drawing.Point(321, 148)
        Me.DO3.Name = "DO3"
        Me.DO3.Size = New System.Drawing.Size(60, 50)
        Me.DO3.TabIndex = 31
        Me.DO3.TabStop = False
        Me.DO3.Tag = "3"
        '
        'Timer1
        '
        Me.Timer1.Interval = 1000
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(10.0!, 19.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(831, 333)
        Me.Controls.Add(Me.DO3)
        Me.Controls.Add(Me.DO2)
        Me.Controls.Add(Me.DO1)
        Me.Controls.Add(Me.DO0)
        Me.Controls.Add(Me.DI3)
        Me.Controls.Add(Me.DI2)
        Me.Controls.Add(Me.DI1)
        Me.Controls.Add(Me.DI0)
        Me.Controls.Add(Me.AO3)
        Me.Controls.Add(Me.AO2)
        Me.Controls.Add(Me.AO1)
        Me.Controls.Add(Me.AO0)
        Me.Controls.Add(Me.AI3)
        Me.Controls.Add(Me.AI2)
        Me.Controls.Add(Me.AI1)
        Me.Controls.Add(Me.AI0)
        Me.Controls.Add(Me.Label9)
        Me.Controls.Add(Me.Label8)
        Me.Controls.Add(Me.Label7)
        Me.Controls.Add(Me.Label6)
        Me.Controls.Add(Me.cmbsb)
        Me.Controls.Add(Me.Label5)
        Me.Controls.Add(Me.cmbpty)
        Me.Controls.Add(Me.Label4)
        Me.Controls.Add(Me.cmbdb)
        Me.Controls.Add(Me.Label3)
        Me.Controls.Add(Me.cmbbaud)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.cmbcom)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.btnClose)
        Me.Controls.Add(Me.btnOpen)
        Me.Font = New System.Drawing.Font("Tahoma", 12.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Margin = New System.Windows.Forms.Padding(4, 5, 4, 5)
        Me.Name = "Form1"
        Me.Text = "Modbus RTU Master"
        CType(Me.DI0, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DI1, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DI2, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DI3, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DO0, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DO1, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DO2, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.DO3, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents btnOpen As System.Windows.Forms.Button
    Friend WithEvents btnClose As System.Windows.Forms.Button
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents cmbcom As System.Windows.Forms.ComboBox
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents cmbbaud As System.Windows.Forms.ComboBox
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents cmbdb As System.Windows.Forms.ComboBox
    Friend WithEvents Label4 As System.Windows.Forms.Label
    Friend WithEvents cmbpty As System.Windows.Forms.ComboBox
    Friend WithEvents Label5 As System.Windows.Forms.Label
    Friend WithEvents cmbsb As System.Windows.Forms.ComboBox
    Friend WithEvents Label6 As System.Windows.Forms.Label
    Friend WithEvents Label7 As System.Windows.Forms.Label
    Friend WithEvents Label8 As System.Windows.Forms.Label
    Friend WithEvents Label9 As System.Windows.Forms.Label
    Friend WithEvents AI0 As System.Windows.Forms.TextBox
    Friend WithEvents AI1 As System.Windows.Forms.TextBox
    Friend WithEvents AI2 As System.Windows.Forms.TextBox
    Friend WithEvents AI3 As System.Windows.Forms.TextBox
    Friend WithEvents AO0 As System.Windows.Forms.TextBox
    Friend WithEvents AO1 As System.Windows.Forms.TextBox
    Friend WithEvents AO2 As System.Windows.Forms.TextBox
    Friend WithEvents AO3 As System.Windows.Forms.TextBox
    Friend WithEvents DI0 As System.Windows.Forms.PictureBox
    Friend WithEvents DI1 As System.Windows.Forms.PictureBox
    Friend WithEvents DI2 As System.Windows.Forms.PictureBox
    Friend WithEvents DI3 As System.Windows.Forms.PictureBox
    Friend WithEvents DO0 As System.Windows.Forms.PictureBox
    Friend WithEvents DO1 As System.Windows.Forms.PictureBox
    Friend WithEvents DO2 As System.Windows.Forms.PictureBox
    Friend WithEvents DO3 As System.Windows.Forms.PictureBox
    Friend WithEvents Timer1 As System.Windows.Forms.Timer

End Class
