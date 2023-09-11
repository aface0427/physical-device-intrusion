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
        Me.pnlCOMStatus = New System.Windows.Forms.Panel
        Me.cmbStopBit = New System.Windows.Forms.ComboBox
        Me.btCloseCOM = New System.Windows.Forms.Button
        Me.cmbParity = New System.Windows.Forms.ComboBox
        Me.btOpenCOM = New System.Windows.Forms.Button
        Me.cmbDataBit = New System.Windows.Forms.ComboBox
        Me.label7 = New System.Windows.Forms.Label
        Me.labStopBit = New System.Windows.Forms.Label
        Me.labParity = New System.Windows.Forms.Label
        Me.labBaud = New System.Windows.Forms.Label
        Me.labDataBit = New System.Windows.Forms.Label
        Me.labPort = New System.Windows.Forms.Label
        Me.cmbBaud = New System.Windows.Forms.ComboBox
        Me.cmbPort = New System.Windows.Forms.ComboBox
        Me.txtAI4 = New System.Windows.Forms.TextBox
        Me.txtAI3 = New System.Windows.Forms.TextBox
        Me.txtAI2 = New System.Windows.Forms.TextBox
        Me.txtAI1 = New System.Windows.Forms.TextBox
        Me.label5 = New System.Windows.Forms.Label
        Me.txtAO4 = New System.Windows.Forms.TextBox
        Me.txtAO3 = New System.Windows.Forms.TextBox
        Me.txtAO2 = New System.Windows.Forms.TextBox
        Me.txtAO1 = New System.Windows.Forms.TextBox
        Me.label3 = New System.Windows.Forms.Label
        Me.label4 = New System.Windows.Forms.Label
        Me.chkDI4 = New System.Windows.Forms.CheckBox
        Me.chkDI3 = New System.Windows.Forms.CheckBox
        Me.chkDI2 = New System.Windows.Forms.CheckBox
        Me.chkDI1 = New System.Windows.Forms.CheckBox
        Me.label2 = New System.Windows.Forms.Label
        Me.chkDO4 = New System.Windows.Forms.CheckBox
        Me.chkDO3 = New System.Windows.Forms.CheckBox
        Me.chkDO2 = New System.Windows.Forms.CheckBox
        Me.chkDO1 = New System.Windows.Forms.CheckBox
        Me.label1 = New System.Windows.Forms.Label
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        Me.pnlCOMStatus.SuspendLayout()
        Me.SuspendLayout()
        '
        'pnlCOMStatus
        '
        Me.pnlCOMStatus.Controls.Add(Me.cmbStopBit)
        Me.pnlCOMStatus.Controls.Add(Me.btCloseCOM)
        Me.pnlCOMStatus.Controls.Add(Me.cmbParity)
        Me.pnlCOMStatus.Controls.Add(Me.btOpenCOM)
        Me.pnlCOMStatus.Controls.Add(Me.cmbDataBit)
        Me.pnlCOMStatus.Controls.Add(Me.label7)
        Me.pnlCOMStatus.Controls.Add(Me.labStopBit)
        Me.pnlCOMStatus.Controls.Add(Me.labParity)
        Me.pnlCOMStatus.Controls.Add(Me.labBaud)
        Me.pnlCOMStatus.Controls.Add(Me.labDataBit)
        Me.pnlCOMStatus.Controls.Add(Me.labPort)
        Me.pnlCOMStatus.Controls.Add(Me.cmbBaud)
        Me.pnlCOMStatus.Controls.Add(Me.cmbPort)
        Me.pnlCOMStatus.Location = New System.Drawing.Point(0, 46)
        Me.pnlCOMStatus.Name = "pnlCOMStatus"
        Me.pnlCOMStatus.Size = New System.Drawing.Size(406, 87)
        Me.pnlCOMStatus.TabIndex = 34
        '
        'cmbStopBit
        '
        Me.cmbStopBit.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.cmbStopBit.Items.AddRange(New Object() {"1", "2"})
        Me.cmbStopBit.Location = New System.Drawing.Point(339, 35)
        Me.cmbStopBit.Name = "cmbStopBit"
        Me.cmbStopBit.Size = New System.Drawing.Size(56, 22)
        Me.cmbStopBit.TabIndex = 32
        '
        'btCloseCOM
        '
        Me.btCloseCOM.Enabled = False
        Me.btCloseCOM.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.btCloseCOM.Location = New System.Drawing.Point(317, 61)
        Me.btCloseCOM.Name = "btCloseCOM"
        Me.btCloseCOM.Size = New System.Drawing.Size(78, 23)
        Me.btCloseCOM.TabIndex = 45
        Me.btCloseCOM.Text = "Close"
        '
        'cmbParity
        '
        Me.cmbParity.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.cmbParity.Items.AddRange(New Object() {"0-None Parity", "1-Odd Parity", "2-Even Parity"})
        Me.cmbParity.Location = New System.Drawing.Point(226, 35)
        Me.cmbParity.Name = "cmbParity"
        Me.cmbParity.Size = New System.Drawing.Size(100, 22)
        Me.cmbParity.TabIndex = 31
        '
        'btOpenCOM
        '
        Me.btOpenCOM.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.btOpenCOM.Location = New System.Drawing.Point(226, 61)
        Me.btOpenCOM.Name = "btOpenCOM"
        Me.btOpenCOM.Size = New System.Drawing.Size(78, 23)
        Me.btOpenCOM.TabIndex = 38
        Me.btOpenCOM.Text = "Open"
        '
        'cmbDataBit
        '
        Me.cmbDataBit.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.cmbDataBit.Items.AddRange(New Object() {"7", "8"})
        Me.cmbDataBit.Location = New System.Drawing.Point(170, 35)
        Me.cmbDataBit.Name = "cmbDataBit"
        Me.cmbDataBit.Size = New System.Drawing.Size(48, 22)
        Me.cmbDataBit.TabIndex = 30
        '
        'label7
        '
        Me.label7.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.label7.ForeColor = System.Drawing.Color.Blue
        Me.label7.Location = New System.Drawing.Point(3, 3)
        Me.label7.Name = "label7"
        Me.label7.Size = New System.Drawing.Size(140, 17)
        Me.label7.TabIndex = 46
        Me.label7.Text = "Connection Status"
        '
        'labStopBit
        '
        Me.labStopBit.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.labStopBit.Location = New System.Drawing.Point(339, 20)
        Me.labStopBit.Name = "labStopBit"
        Me.labStopBit.Size = New System.Drawing.Size(56, 15)
        Me.labStopBit.TabIndex = 47
        Me.labStopBit.Text = "Stop Bit"
        Me.labStopBit.TextAlign = System.Drawing.ContentAlignment.TopCenter
        '
        'labParity
        '
        Me.labParity.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.labParity.Location = New System.Drawing.Point(228, 20)
        Me.labParity.Name = "labParity"
        Me.labParity.Size = New System.Drawing.Size(98, 15)
        Me.labParity.TabIndex = 48
        Me.labParity.Text = "Parity"
        Me.labParity.TextAlign = System.Drawing.ContentAlignment.TopCenter
        '
        'labBaud
        '
        Me.labBaud.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.labBaud.Location = New System.Drawing.Point(86, 20)
        Me.labBaud.Name = "labBaud"
        Me.labBaud.Size = New System.Drawing.Size(75, 15)
        Me.labBaud.TabIndex = 49
        Me.labBaud.Text = "Baudrate"
        Me.labBaud.TextAlign = System.Drawing.ContentAlignment.TopCenter
        '
        'labDataBit
        '
        Me.labDataBit.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.labDataBit.Location = New System.Drawing.Point(170, 20)
        Me.labDataBit.Name = "labDataBit"
        Me.labDataBit.Size = New System.Drawing.Size(48, 15)
        Me.labDataBit.TabIndex = 50
        Me.labDataBit.Text = "Data Bit"
        Me.labDataBit.TextAlign = System.Drawing.ContentAlignment.TopCenter
        '
        'labPort
        '
        Me.labPort.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.labPort.Location = New System.Drawing.Point(6, 20)
        Me.labPort.Name = "labPort"
        Me.labPort.Size = New System.Drawing.Size(75, 15)
        Me.labPort.TabIndex = 51
        Me.labPort.Text = "COM Port"
        Me.labPort.TextAlign = System.Drawing.ContentAlignment.TopCenter
        '
        'cmbBaud
        '
        Me.cmbBaud.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.cmbBaud.Items.AddRange(New Object() {"1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"})
        Me.cmbBaud.Location = New System.Drawing.Point(85, 35)
        Me.cmbBaud.Name = "cmbBaud"
        Me.cmbBaud.Size = New System.Drawing.Size(76, 22)
        Me.cmbBaud.TabIndex = 29
        '
        'cmbPort
        '
        Me.cmbPort.Font = New System.Drawing.Font("Arial", 8.0!)
        Me.cmbPort.Location = New System.Drawing.Point(6, 35)
        Me.cmbPort.Name = "cmbPort"
        Me.cmbPort.Size = New System.Drawing.Size(75, 22)
        Me.cmbPort.TabIndex = 28
        '
        'txtAI4
        '
        Me.txtAI4.Location = New System.Drawing.Point(191, 300)
        Me.txtAI4.Name = "txtAI4"
        Me.txtAI4.Size = New System.Drawing.Size(98, 22)
        Me.txtAI4.TabIndex = 50
        Me.txtAI4.Text = "444"
        '
        'txtAI3
        '
        Me.txtAI3.Location = New System.Drawing.Point(191, 259)
        Me.txtAI3.Name = "txtAI3"
        Me.txtAI3.Size = New System.Drawing.Size(98, 22)
        Me.txtAI3.TabIndex = 49
        Me.txtAI3.Text = "333"
        '
        'txtAI2
        '
        Me.txtAI2.Location = New System.Drawing.Point(191, 218)
        Me.txtAI2.Name = "txtAI2"
        Me.txtAI2.Size = New System.Drawing.Size(98, 22)
        Me.txtAI2.TabIndex = 48
        Me.txtAI2.Text = "222"
        '
        'txtAI1
        '
        Me.txtAI1.Location = New System.Drawing.Point(191, 178)
        Me.txtAI1.Name = "txtAI1"
        Me.txtAI1.Size = New System.Drawing.Size(98, 22)
        Me.txtAI1.TabIndex = 47
        Me.txtAI1.Text = "111"
        '
        'label5
        '
        Me.label5.Font = New System.Drawing.Font("Tahoma", 24.0!)
        Me.label5.Location = New System.Drawing.Point(44, 9)
        Me.label5.Name = "label5"
        Me.label5.Size = New System.Drawing.Size(394, 34)
        Me.label5.TabIndex = 51
        Me.label5.Text = "IO Simulation"
        '
        'txtAO4
        '
        Me.txtAO4.Location = New System.Drawing.Point(308, 300)
        Me.txtAO4.Name = "txtAO4"
        Me.txtAO4.Size = New System.Drawing.Size(98, 22)
        Me.txtAO4.TabIndex = 46
        Me.txtAO4.Text = "0"
        '
        'txtAO3
        '
        Me.txtAO3.Location = New System.Drawing.Point(308, 259)
        Me.txtAO3.Name = "txtAO3"
        Me.txtAO3.Size = New System.Drawing.Size(98, 22)
        Me.txtAO3.TabIndex = 45
        Me.txtAO3.Text = "0"
        '
        'txtAO2
        '
        Me.txtAO2.Location = New System.Drawing.Point(308, 218)
        Me.txtAO2.Name = "txtAO2"
        Me.txtAO2.Size = New System.Drawing.Size(98, 22)
        Me.txtAO2.TabIndex = 44
        Me.txtAO2.Text = "0"
        '
        'txtAO1
        '
        Me.txtAO1.Location = New System.Drawing.Point(308, 178)
        Me.txtAO1.Name = "txtAO1"
        Me.txtAO1.Size = New System.Drawing.Size(98, 22)
        Me.txtAO1.TabIndex = 43
        Me.txtAO1.Text = "0"
        '
        'label3
        '
        Me.label3.Location = New System.Drawing.Point(306, 153)
        Me.label3.Name = "label3"
        Me.label3.Size = New System.Drawing.Size(122, 21)
        Me.label3.TabIndex = 52
        Me.label3.Text = "AO Value"
        '
        'label4
        '
        Me.label4.Location = New System.Drawing.Point(191, 153)
        Me.label4.Name = "label4"
        Me.label4.Size = New System.Drawing.Size(109, 21)
        Me.label4.TabIndex = 53
        Me.label4.Text = "AI Value"
        '
        'chkDI4
        '
        Me.chkDI4.Location = New System.Drawing.Point(103, 300)
        Me.chkDI4.Name = "chkDI4"
        Me.chkDI4.Size = New System.Drawing.Size(82, 23)
        Me.chkDI4.TabIndex = 42
        Me.chkDI4.Text = "100004"
        '
        'chkDI3
        '
        Me.chkDI3.Location = New System.Drawing.Point(103, 259)
        Me.chkDI3.Name = "chkDI3"
        Me.chkDI3.Size = New System.Drawing.Size(82, 23)
        Me.chkDI3.TabIndex = 41
        Me.chkDI3.Text = "100003"
        '
        'chkDI2
        '
        Me.chkDI2.Location = New System.Drawing.Point(103, 218)
        Me.chkDI2.Name = "chkDI2"
        Me.chkDI2.Size = New System.Drawing.Size(82, 23)
        Me.chkDI2.TabIndex = 40
        Me.chkDI2.Text = "100002"
        '
        'chkDI1
        '
        Me.chkDI1.Location = New System.Drawing.Point(101, 177)
        Me.chkDI1.Name = "chkDI1"
        Me.chkDI1.Size = New System.Drawing.Size(82, 23)
        Me.chkDI1.TabIndex = 39
        Me.chkDI1.Text = "100001"
        '
        'label2
        '
        Me.label2.Location = New System.Drawing.Point(103, 153)
        Me.label2.Name = "label2"
        Me.label2.Size = New System.Drawing.Size(82, 21)
        Me.label2.TabIndex = 54
        Me.label2.Text = "DI Value"
        '
        'chkDO4
        '
        Me.chkDO4.Location = New System.Drawing.Point(15, 300)
        Me.chkDO4.Name = "chkDO4"
        Me.chkDO4.Size = New System.Drawing.Size(82, 23)
        Me.chkDO4.TabIndex = 38
        Me.chkDO4.Text = "000004"
        '
        'chkDO3
        '
        Me.chkDO3.Location = New System.Drawing.Point(15, 259)
        Me.chkDO3.Name = "chkDO3"
        Me.chkDO3.Size = New System.Drawing.Size(82, 23)
        Me.chkDO3.TabIndex = 37
        Me.chkDO3.Text = "000003"
        '
        'chkDO2
        '
        Me.chkDO2.Location = New System.Drawing.Point(15, 218)
        Me.chkDO2.Name = "chkDO2"
        Me.chkDO2.Size = New System.Drawing.Size(82, 23)
        Me.chkDO2.TabIndex = 36
        Me.chkDO2.Text = "000002"
        '
        'chkDO1
        '
        Me.chkDO1.Location = New System.Drawing.Point(13, 177)
        Me.chkDO1.Name = "chkDO1"
        Me.chkDO1.Size = New System.Drawing.Size(82, 23)
        Me.chkDO1.TabIndex = 35
        Me.chkDO1.Text = "000001"
        '
        'label1
        '
        Me.label1.Location = New System.Drawing.Point(15, 153)
        Me.label1.Name = "label1"
        Me.label1.Size = New System.Drawing.Size(82, 21)
        Me.label1.TabIndex = 55
        Me.label1.Text = "DO Value"
        '
        'Timer1
        '
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 12.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(435, 338)
        Me.Controls.Add(Me.pnlCOMStatus)
        Me.Controls.Add(Me.txtAI4)
        Me.Controls.Add(Me.txtAI3)
        Me.Controls.Add(Me.txtAI2)
        Me.Controls.Add(Me.txtAI1)
        Me.Controls.Add(Me.label5)
        Me.Controls.Add(Me.txtAO4)
        Me.Controls.Add(Me.txtAO3)
        Me.Controls.Add(Me.txtAO2)
        Me.Controls.Add(Me.txtAO1)
        Me.Controls.Add(Me.label3)
        Me.Controls.Add(Me.label4)
        Me.Controls.Add(Me.chkDI4)
        Me.Controls.Add(Me.chkDI3)
        Me.Controls.Add(Me.chkDI2)
        Me.Controls.Add(Me.chkDI1)
        Me.Controls.Add(Me.label2)
        Me.Controls.Add(Me.chkDO4)
        Me.Controls.Add(Me.chkDO3)
        Me.Controls.Add(Me.chkDO2)
        Me.Controls.Add(Me.chkDO1)
        Me.Controls.Add(Me.label1)
        Me.Name = "Form1"
        Me.Text = "Modbus_Slave_RTU_Demo"
        Me.pnlCOMStatus.ResumeLayout(False)
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Private WithEvents pnlCOMStatus As System.Windows.Forms.Panel
    Private WithEvents cmbStopBit As System.Windows.Forms.ComboBox
    Private WithEvents btCloseCOM As System.Windows.Forms.Button
    Private WithEvents cmbParity As System.Windows.Forms.ComboBox
    Private WithEvents btOpenCOM As System.Windows.Forms.Button
    Private WithEvents cmbDataBit As System.Windows.Forms.ComboBox
    Private WithEvents label7 As System.Windows.Forms.Label
    Private WithEvents labStopBit As System.Windows.Forms.Label
    Private WithEvents labParity As System.Windows.Forms.Label
    Private WithEvents labBaud As System.Windows.Forms.Label
    Private WithEvents labDataBit As System.Windows.Forms.Label
    Private WithEvents labPort As System.Windows.Forms.Label
    Private WithEvents cmbBaud As System.Windows.Forms.ComboBox
    Private WithEvents cmbPort As System.Windows.Forms.ComboBox
    Private WithEvents txtAI4 As System.Windows.Forms.TextBox
    Private WithEvents txtAI3 As System.Windows.Forms.TextBox
    Private WithEvents txtAI2 As System.Windows.Forms.TextBox
    Private WithEvents txtAI1 As System.Windows.Forms.TextBox
    Private WithEvents label5 As System.Windows.Forms.Label
    Private WithEvents txtAO4 As System.Windows.Forms.TextBox
    Private WithEvents txtAO3 As System.Windows.Forms.TextBox
    Private WithEvents txtAO2 As System.Windows.Forms.TextBox
    Private WithEvents txtAO1 As System.Windows.Forms.TextBox
    Private WithEvents label3 As System.Windows.Forms.Label
    Private WithEvents label4 As System.Windows.Forms.Label
    Private WithEvents chkDI4 As System.Windows.Forms.CheckBox
    Private WithEvents chkDI3 As System.Windows.Forms.CheckBox
    Private WithEvents chkDI2 As System.Windows.Forms.CheckBox
    Private WithEvents chkDI1 As System.Windows.Forms.CheckBox
    Private WithEvents label2 As System.Windows.Forms.Label
    Private WithEvents chkDO4 As System.Windows.Forms.CheckBox
    Private WithEvents chkDO3 As System.Windows.Forms.CheckBox
    Private WithEvents chkDO2 As System.Windows.Forms.CheckBox
    Private WithEvents chkDO1 As System.Windows.Forms.CheckBox
    Private WithEvents label1 As System.Windows.Forms.Label
    Friend WithEvents Timer1 As System.Windows.Forms.Timer

End Class
