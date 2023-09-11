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
        Me.labServerName = New System.Windows.Forms.Label
        Me.btnStop = New System.Windows.Forms.Button
        Me.btnStart = New System.Windows.Forms.Button
        Me.txtAI3 = New System.Windows.Forms.TextBox
        Me.txtAI2 = New System.Windows.Forms.TextBox
        Me.txtAI1 = New System.Windows.Forms.TextBox
        Me.txtAI4 = New System.Windows.Forms.TextBox
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
        Me.SuspendLayout()
        '
        'labServerName
        '
        Me.labServerName.Location = New System.Drawing.Point(231, 46)
        Me.labServerName.Name = "labServerName"
        Me.labServerName.Size = New System.Drawing.Size(203, 20)
        Me.labServerName.TabIndex = 63
        Me.labServerName.Text = "label6"
        '
        'btnStop
        '
        Me.btnStop.Enabled = False
        Me.btnStop.Location = New System.Drawing.Point(332, 15)
        Me.btnStop.Name = "btnStop"
        Me.btnStop.Size = New System.Drawing.Size(98, 28)
        Me.btnStop.TabIndex = 81
        Me.btnStop.Text = "stop"
        '
        'btnStart
        '
        Me.btnStart.Location = New System.Drawing.Point(228, 15)
        Me.btnStart.Name = "btnStart"
        Me.btnStart.Size = New System.Drawing.Size(98, 28)
        Me.btnStart.TabIndex = 80
        Me.btnStart.Text = "start"
        '
        'txtAI3
        '
        Me.txtAI3.Location = New System.Drawing.Point(203, 181)
        Me.txtAI3.Name = "txtAI3"
        Me.txtAI3.Size = New System.Drawing.Size(98, 22)
        Me.txtAI3.TabIndex = 78
        Me.txtAI3.Text = "333"
        '
        'txtAI2
        '
        Me.txtAI2.Location = New System.Drawing.Point(203, 140)
        Me.txtAI2.Name = "txtAI2"
        Me.txtAI2.Size = New System.Drawing.Size(98, 22)
        Me.txtAI2.TabIndex = 77
        Me.txtAI2.Text = "222"
        '
        'txtAI1
        '
        Me.txtAI1.Location = New System.Drawing.Point(203, 100)
        Me.txtAI1.Name = "txtAI1"
        Me.txtAI1.Size = New System.Drawing.Size(98, 22)
        Me.txtAI1.TabIndex = 76
        Me.txtAI1.Text = "111"
        '
        'txtAI4
        '
        Me.txtAI4.Location = New System.Drawing.Point(203, 222)
        Me.txtAI4.Name = "txtAI4"
        Me.txtAI4.Size = New System.Drawing.Size(98, 22)
        Me.txtAI4.TabIndex = 79
        Me.txtAI4.Text = "444"
        '
        'label5
        '
        Me.label5.Font = New System.Drawing.Font("Tahoma", 24.0!)
        Me.label5.Location = New System.Drawing.Point(12, 9)
        Me.label5.Name = "label5"
        Me.label5.Size = New System.Drawing.Size(210, 34)
        Me.label5.TabIndex = 82
        Me.label5.Text = "IO Simulation"
        '
        'txtAO4
        '
        Me.txtAO4.Location = New System.Drawing.Point(332, 222)
        Me.txtAO4.Name = "txtAO4"
        Me.txtAO4.Size = New System.Drawing.Size(98, 22)
        Me.txtAO4.TabIndex = 75
        Me.txtAO4.Text = "0"
        '
        'txtAO3
        '
        Me.txtAO3.Location = New System.Drawing.Point(332, 181)
        Me.txtAO3.Name = "txtAO3"
        Me.txtAO3.Size = New System.Drawing.Size(98, 22)
        Me.txtAO3.TabIndex = 74
        Me.txtAO3.Text = "0"
        '
        'txtAO2
        '
        Me.txtAO2.Location = New System.Drawing.Point(332, 140)
        Me.txtAO2.Name = "txtAO2"
        Me.txtAO2.Size = New System.Drawing.Size(98, 22)
        Me.txtAO2.TabIndex = 73
        Me.txtAO2.Text = "0"
        '
        'txtAO1
        '
        Me.txtAO1.Location = New System.Drawing.Point(332, 100)
        Me.txtAO1.Name = "txtAO1"
        Me.txtAO1.Size = New System.Drawing.Size(98, 22)
        Me.txtAO1.TabIndex = 72
        Me.txtAO1.Text = "0"
        '
        'label3
        '
        Me.label3.Location = New System.Drawing.Point(330, 75)
        Me.label3.Name = "label3"
        Me.label3.Size = New System.Drawing.Size(100, 21)
        Me.label3.TabIndex = 83
        Me.label3.Text = "AO Value"
        '
        'label4
        '
        Me.label4.Location = New System.Drawing.Point(203, 75)
        Me.label4.Name = "label4"
        Me.label4.Size = New System.Drawing.Size(109, 21)
        Me.label4.TabIndex = 84
        Me.label4.Text = "AI Value"
        '
        'chkDI4
        '
        Me.chkDI4.Location = New System.Drawing.Point(100, 222)
        Me.chkDI4.Name = "chkDI4"
        Me.chkDI4.Size = New System.Drawing.Size(82, 23)
        Me.chkDI4.TabIndex = 71
        Me.chkDI4.Text = "100004"
        '
        'chkDI3
        '
        Me.chkDI3.Location = New System.Drawing.Point(100, 181)
        Me.chkDI3.Name = "chkDI3"
        Me.chkDI3.Size = New System.Drawing.Size(82, 23)
        Me.chkDI3.TabIndex = 70
        Me.chkDI3.Text = "100003"
        '
        'chkDI2
        '
        Me.chkDI2.Location = New System.Drawing.Point(100, 140)
        Me.chkDI2.Name = "chkDI2"
        Me.chkDI2.Size = New System.Drawing.Size(82, 23)
        Me.chkDI2.TabIndex = 69
        Me.chkDI2.Text = "100002"
        '
        'chkDI1
        '
        Me.chkDI1.Location = New System.Drawing.Point(98, 99)
        Me.chkDI1.Name = "chkDI1"
        Me.chkDI1.Size = New System.Drawing.Size(82, 23)
        Me.chkDI1.TabIndex = 68
        Me.chkDI1.Text = "100001"
        '
        'label2
        '
        Me.label2.Location = New System.Drawing.Point(100, 75)
        Me.label2.Name = "label2"
        Me.label2.Size = New System.Drawing.Size(82, 21)
        Me.label2.TabIndex = 85
        Me.label2.Text = "DI Value"
        '
        'chkDO4
        '
        Me.chkDO4.Location = New System.Drawing.Point(12, 222)
        Me.chkDO4.Name = "chkDO4"
        Me.chkDO4.Size = New System.Drawing.Size(82, 23)
        Me.chkDO4.TabIndex = 67
        Me.chkDO4.Text = "000004"
        '
        'chkDO3
        '
        Me.chkDO3.Location = New System.Drawing.Point(12, 181)
        Me.chkDO3.Name = "chkDO3"
        Me.chkDO3.Size = New System.Drawing.Size(82, 23)
        Me.chkDO3.TabIndex = 66
        Me.chkDO3.Text = "000003"
        '
        'chkDO2
        '
        Me.chkDO2.Location = New System.Drawing.Point(12, 140)
        Me.chkDO2.Name = "chkDO2"
        Me.chkDO2.Size = New System.Drawing.Size(82, 23)
        Me.chkDO2.TabIndex = 65
        Me.chkDO2.Text = "000002"
        '
        'chkDO1
        '
        Me.chkDO1.Location = New System.Drawing.Point(10, 99)
        Me.chkDO1.Name = "chkDO1"
        Me.chkDO1.Size = New System.Drawing.Size(82, 23)
        Me.chkDO1.TabIndex = 64
        Me.chkDO1.Text = "000001"
        '
        'label1
        '
        Me.label1.Location = New System.Drawing.Point(12, 75)
        Me.label1.Name = "label1"
        Me.label1.Size = New System.Drawing.Size(82, 21)
        Me.label1.TabIndex = 86
        Me.label1.Text = "DO Value"
        '
        'Timer1
        '
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 12.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(447, 269)
        Me.Controls.Add(Me.labServerName)
        Me.Controls.Add(Me.btnStop)
        Me.Controls.Add(Me.btnStart)
        Me.Controls.Add(Me.txtAI3)
        Me.Controls.Add(Me.txtAI2)
        Me.Controls.Add(Me.txtAI1)
        Me.Controls.Add(Me.txtAI4)
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
        Me.Text = "Modbus_Slave_TCP_Demo"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Private WithEvents labServerName As System.Windows.Forms.Label
    Private WithEvents btnStop As System.Windows.Forms.Button
    Private WithEvents btnStart As System.Windows.Forms.Button
    Private WithEvents txtAI3 As System.Windows.Forms.TextBox
    Private WithEvents txtAI2 As System.Windows.Forms.TextBox
    Private WithEvents txtAI1 As System.Windows.Forms.TextBox
    Private WithEvents txtAI4 As System.Windows.Forms.TextBox
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
