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
        Me.txtIP = New System.Windows.Forms.TextBox
        Me.Label1 = New System.Windows.Forms.Label
        Me.btnStart = New System.Windows.Forms.Button
        Me.btnStop = New System.Windows.Forms.Button
        Me.Label2 = New System.Windows.Forms.Label
        Me.Label3 = New System.Windows.Forms.Label
        Me.Label4 = New System.Windows.Forms.Label
        Me.Label5 = New System.Windows.Forms.Label
        Me.DI0 = New System.Windows.Forms.PictureBox
        Me.DI1 = New System.Windows.Forms.PictureBox
        Me.DI2 = New System.Windows.Forms.PictureBox
        Me.DI3 = New System.Windows.Forms.PictureBox
        Me.DO0 = New System.Windows.Forms.PictureBox
        Me.DO1 = New System.Windows.Forms.PictureBox
        Me.DO2 = New System.Windows.Forms.PictureBox
        Me.DO3 = New System.Windows.Forms.PictureBox
        Me.AI0 = New System.Windows.Forms.TextBox
        Me.AI1 = New System.Windows.Forms.TextBox
        Me.AI2 = New System.Windows.Forms.TextBox
        Me.AI3 = New System.Windows.Forms.TextBox
        Me.AO0 = New System.Windows.Forms.TextBox
        Me.AO1 = New System.Windows.Forms.TextBox
        Me.AO2 = New System.Windows.Forms.TextBox
        Me.AO3 = New System.Windows.Forms.TextBox
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
        'txtIP
        '
        Me.txtIP.Location = New System.Drawing.Point(134, 17)
        Me.txtIP.Margin = New System.Windows.Forms.Padding(6)
        Me.txtIP.Name = "txtIP"
        Me.txtIP.Size = New System.Drawing.Size(196, 30)
        Me.txtIP.TabIndex = 0
        Me.txtIP.Text = "10.0.0.69"
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(12, 20)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(113, 23)
        Me.Label1.TabIndex = 1
        Me.Label1.Text = "IP Address"
        '
        'btnStart
        '
        Me.btnStart.Location = New System.Drawing.Point(365, 7)
        Me.btnStart.Name = "btnStart"
        Me.btnStart.Size = New System.Drawing.Size(95, 40)
        Me.btnStart.TabIndex = 2
        Me.btnStart.Text = "Start"
        Me.btnStart.UseVisualStyleBackColor = True
        '
        'btnStop
        '
        Me.btnStop.Location = New System.Drawing.Point(479, 7)
        Me.btnStop.Name = "btnStop"
        Me.btnStop.Size = New System.Drawing.Size(95, 40)
        Me.btnStop.TabIndex = 3
        Me.btnStop.Text = "Stop"
        Me.btnStop.UseVisualStyleBackColor = True
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(12, 84)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(33, 23)
        Me.Label2.TabIndex = 4
        Me.Label2.Text = "DI"
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(12, 153)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(39, 23)
        Me.Label3.TabIndex = 5
        Me.Label3.Text = "DO"
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.Location = New System.Drawing.Point(12, 225)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(32, 23)
        Me.Label4.TabIndex = 6
        Me.Label4.Text = "AI"
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(12, 292)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(38, 23)
        Me.Label5.TabIndex = 7
        Me.Label5.Text = "AO"
        '
        'DI0
        '
        Me.DI0.BackColor = System.Drawing.Color.Green
        Me.DI0.Location = New System.Drawing.Point(63, 73)
        Me.DI0.Name = "DI0"
        Me.DI0.Size = New System.Drawing.Size(51, 48)
        Me.DI0.TabIndex = 8
        Me.DI0.TabStop = False
        '
        'DI1
        '
        Me.DI1.BackColor = System.Drawing.Color.Green
        Me.DI1.Location = New System.Drawing.Point(134, 73)
        Me.DI1.Name = "DI1"
        Me.DI1.Size = New System.Drawing.Size(51, 48)
        Me.DI1.TabIndex = 9
        Me.DI1.TabStop = False
        '
        'DI2
        '
        Me.DI2.BackColor = System.Drawing.Color.Green
        Me.DI2.Location = New System.Drawing.Point(211, 73)
        Me.DI2.Name = "DI2"
        Me.DI2.Size = New System.Drawing.Size(51, 48)
        Me.DI2.TabIndex = 10
        Me.DI2.TabStop = False
        '
        'DI3
        '
        Me.DI3.BackColor = System.Drawing.Color.Green
        Me.DI3.Location = New System.Drawing.Point(288, 73)
        Me.DI3.Name = "DI3"
        Me.DI3.Size = New System.Drawing.Size(51, 48)
        Me.DI3.TabIndex = 11
        Me.DI3.TabStop = False
        '
        'DO0
        '
        Me.DO0.BackColor = System.Drawing.Color.Maroon
        Me.DO0.Location = New System.Drawing.Point(63, 141)
        Me.DO0.Name = "DO0"
        Me.DO0.Size = New System.Drawing.Size(51, 48)
        Me.DO0.TabIndex = 12
        Me.DO0.TabStop = False
        Me.DO0.Tag = "0"
        '
        'DO1
        '
        Me.DO1.BackColor = System.Drawing.Color.Maroon
        Me.DO1.Location = New System.Drawing.Point(134, 141)
        Me.DO1.Name = "DO1"
        Me.DO1.Size = New System.Drawing.Size(51, 48)
        Me.DO1.TabIndex = 13
        Me.DO1.TabStop = False
        Me.DO1.Tag = "1"
        '
        'DO2
        '
        Me.DO2.BackColor = System.Drawing.Color.Maroon
        Me.DO2.Location = New System.Drawing.Point(211, 141)
        Me.DO2.Name = "DO2"
        Me.DO2.Size = New System.Drawing.Size(51, 48)
        Me.DO2.TabIndex = 14
        Me.DO2.TabStop = False
        Me.DO2.Tag = "2"
        '
        'DO3
        '
        Me.DO3.BackColor = System.Drawing.Color.Maroon
        Me.DO3.Location = New System.Drawing.Point(288, 141)
        Me.DO3.Name = "DO3"
        Me.DO3.Size = New System.Drawing.Size(51, 48)
        Me.DO3.TabIndex = 15
        Me.DO3.TabStop = False
        Me.DO3.Tag = "3"
        '
        'AI0
        '
        Me.AI0.Location = New System.Drawing.Point(63, 222)
        Me.AI0.Name = "AI0"
        Me.AI0.Size = New System.Drawing.Size(83, 30)
        Me.AI0.TabIndex = 16
        '
        'AI1
        '
        Me.AI1.Location = New System.Drawing.Point(169, 222)
        Me.AI1.Name = "AI1"
        Me.AI1.Size = New System.Drawing.Size(83, 30)
        Me.AI1.TabIndex = 17
        '
        'AI2
        '
        Me.AI2.Location = New System.Drawing.Point(275, 222)
        Me.AI2.Name = "AI2"
        Me.AI2.Size = New System.Drawing.Size(83, 30)
        Me.AI2.TabIndex = 18
        '
        'AI3
        '
        Me.AI3.Location = New System.Drawing.Point(377, 222)
        Me.AI3.Name = "AI3"
        Me.AI3.Size = New System.Drawing.Size(83, 30)
        Me.AI3.TabIndex = 19
        '
        'AO0
        '
        Me.AO0.Location = New System.Drawing.Point(63, 285)
        Me.AO0.Name = "AO0"
        Me.AO0.Size = New System.Drawing.Size(83, 30)
        Me.AO0.TabIndex = 20
        Me.AO0.Tag = "0"
        '
        'AO1
        '
        Me.AO1.Location = New System.Drawing.Point(169, 285)
        Me.AO1.Name = "AO1"
        Me.AO1.Size = New System.Drawing.Size(83, 30)
        Me.AO1.TabIndex = 21
        Me.AO1.Tag = "1"
        '
        'AO2
        '
        Me.AO2.Location = New System.Drawing.Point(275, 285)
        Me.AO2.Name = "AO2"
        Me.AO2.Size = New System.Drawing.Size(83, 30)
        Me.AO2.TabIndex = 22
        Me.AO2.Tag = "2"
        '
        'AO3
        '
        Me.AO3.Location = New System.Drawing.Point(377, 285)
        Me.AO3.Name = "AO3"
        Me.AO3.Size = New System.Drawing.Size(83, 30)
        Me.AO3.TabIndex = 23
        Me.AO3.Tag = "3"
        '
        'Timer1
        '
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(12.0!, 23.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(586, 349)
        Me.Controls.Add(Me.AO3)
        Me.Controls.Add(Me.AO2)
        Me.Controls.Add(Me.AO1)
        Me.Controls.Add(Me.AO0)
        Me.Controls.Add(Me.AI3)
        Me.Controls.Add(Me.AI2)
        Me.Controls.Add(Me.AI1)
        Me.Controls.Add(Me.AI0)
        Me.Controls.Add(Me.DO3)
        Me.Controls.Add(Me.DO2)
        Me.Controls.Add(Me.DO1)
        Me.Controls.Add(Me.DO0)
        Me.Controls.Add(Me.DI3)
        Me.Controls.Add(Me.DI2)
        Me.Controls.Add(Me.DI1)
        Me.Controls.Add(Me.DI0)
        Me.Controls.Add(Me.Label5)
        Me.Controls.Add(Me.Label4)
        Me.Controls.Add(Me.Label3)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.btnStop)
        Me.Controls.Add(Me.btnStart)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.txtIP)
        Me.Font = New System.Drawing.Font("Tahoma", 14.25!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Margin = New System.Windows.Forms.Padding(6)
        Me.Name = "Form1"
        Me.Text = "Form1"
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
    Friend WithEvents txtIP As System.Windows.Forms.TextBox
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents btnStart As System.Windows.Forms.Button
    Friend WithEvents btnStop As System.Windows.Forms.Button
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents Label4 As System.Windows.Forms.Label
    Friend WithEvents Label5 As System.Windows.Forms.Label
    Friend WithEvents DI0 As System.Windows.Forms.PictureBox
    Friend WithEvents DI1 As System.Windows.Forms.PictureBox
    Friend WithEvents DI2 As System.Windows.Forms.PictureBox
    Friend WithEvents DI3 As System.Windows.Forms.PictureBox
    Friend WithEvents DO0 As System.Windows.Forms.PictureBox
    Friend WithEvents DO1 As System.Windows.Forms.PictureBox
    Friend WithEvents DO2 As System.Windows.Forms.PictureBox
    Friend WithEvents DO3 As System.Windows.Forms.PictureBox
    Friend WithEvents AI0 As System.Windows.Forms.TextBox
    Friend WithEvents AI1 As System.Windows.Forms.TextBox
    Friend WithEvents AI2 As System.Windows.Forms.TextBox
    Friend WithEvents AI3 As System.Windows.Forms.TextBox
    Friend WithEvents AO0 As System.Windows.Forms.TextBox
    Friend WithEvents AO1 As System.Windows.Forms.TextBox
    Friend WithEvents AO2 As System.Windows.Forms.TextBox
    Friend WithEvents AO3 As System.Windows.Forms.TextBox
    Friend WithEvents Timer1 As System.Windows.Forms.Timer

End Class
