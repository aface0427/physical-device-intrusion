Imports System
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Text
Imports System.Windows.Forms
Imports System.IO.Ports
Imports Modbus
Imports Modbus.Device
Imports Modbus.Data

Public Class Form1

    Private slave As ModbusSlave
    Private comPort As New SerialPort() 'create new comPort object
    Private slaveID As Byte = 1
    Private Sub Modbue_Request_Event(ByVal sender As Object, ByVal e As Modbus.Device.ModbusSlaveRequestEventArgs)
        'request from master
        Dim fc As Byte = e.Message.FunctionCode
        Dim data() As Byte = e.Message.MessageFrame
        Dim byteStartaddress() As Byte = {data(3), data(2)}
        Dim byteNum() As Byte = {data(5), data(4)}
        Dim startAddress As Short = BitConverter.ToInt16(byteStartAddress, 0)
        Dim NumOfPoint As Short = BitConverter.ToInt16(byteNum, 0)
        Console.WriteLine(fc.ToString() + "," + startAddress.ToString() + "," + NumOfPoint.ToString())
    End Sub
    Private Sub Modbus_DataStoreWriteTo(ByVal sender As Object, ByVal e As Modbus.Data.DataStoreEventArgs)
        Dim iAddress As Integer = e.StartAddress
        Select Case e.ModbusDataType
            Case ModbusDataType.Coil
                For i As Integer = 0 To e.Data.A.Count - 1
                    'Set DO

                    'e.Data.A(i) already write to slave.DataStore.CoilDiscretes(e.StartAddress + i + 1)
                    'e.StartAddress starts from 0
                    'You can set DO value to hardware here
                    DoDOUpdate(iAddress, e.Data.A(i)) 'call DoDOUpdate() to update DO value
                    iAddress += 1
                    If e.Data.A.Count = 1 Then
                        Exit For
                    End If
                Next i
                Exit Select
            Case ModbusDataType.HoldingRegister
                For i As Integer = 0 To e.Data.B.Count - 1
                    'Set AO                 

                    'e.Data.B(i) already write to slave.DataStore.HoldingRegisters(e.StartAddress + i + 1)
                    'e.StartAddress starts from 0
                    'You can set AO value to hardware here
                    DoAOUpdate(iAddress, e.Data.B(i).ToString()) 'call DoAOUpdate to update AO value
                    iAddress += 1
                    If e.Data.B.Count = 1 Then
                        Exit For
                    End If
                Next i
                Exit Select
        End Select
    End Sub
#Region "Set AO"
    Private Delegate Sub UpdateAOStatusDelegate(ByVal index As Integer, ByVal value As String)
    Private Sub DoAOUpdate(ByVal index As Integer, ByVal value As String)
        If Me.InvokeRequired = True Then
            ' we were called on a worker thread
            ' marshal the call to the user interface thread
            Me.Invoke(New UpdateAOStatusDelegate(AddressOf DoAOUpdate), New Object() {index, value})
            Return
        End If
        'this code can only be reached
        ' by the user interface thread
        Select Case index
            Case 0
                Me.txtAO1.Text = value
                Exit Select
            Case 1
                Me.txtAO2.Text = value
                Exit Select
            Case 2
                Me.txtAO3.Text = value
                Exit Select
            Case 3
                Me.txtAO4.Text = value
                Exit Select

        End Select
    End Sub
#End Region

#Region "Set DO"
    Private Delegate Sub UpdateDOStatusDelegate(ByVal index As Integer, ByVal value As Boolean)
    Private Sub DoDOUpdate(ByVal index As Integer, ByVal value As Boolean)
        If Me.InvokeRequired = True Then
            ' we were called on a worker thread
            ' marshal the call to the user interface thread
            Me.Invoke(New UpdateDOStatusDelegate(AddressOf DoDOUpdate), New Object() {index, value})
            Return
        End If
        'this code can only be reached
        ' by the user interface thread
        Select Case index
            Case 0
                Me.chkDO1.Checked = value
                Exit Select
            Case 1
                Me.chkDO2.Checked = value
                Exit Select
            Case 2
                Me.chkDO3.Checked = value
                Exit Select
            Case 3
                Me.chkDO4.Checked = value
                Exit Select
        End Select

    End Sub
#End Region

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As EventArgs) Handles MyBase.Load
        cmbBaud.SelectedIndex = 7
        cmbDataBit.SelectedIndex = 1
        cmbParity.SelectedIndex = 0
        cmbStopBit.SelectedIndex = 0
        For Each s As String In SerialPort.GetPortNames()
            cmbPort.Items.Add(s)
        Next
        cmbPort.SelectedIndex = 0
        btOpenCOM.Enabled = True
        btCloseCOM.Enabled = False
    End Sub

    Private Sub btOpenCOM_Click(ByVal sender As System.Object, ByVal e As EventArgs) Handles btOpenCOM.Click
        'start RTU slave
        comPort.PortName = cmbPort.Text
        comPort.BaudRate = Integer.Parse(cmbBaud.SelectedItem.ToString())
        If cmbParity.SelectedIndex = 0 Then
            comPort.Parity = Parity.None
        ElseIf cmbParity.SelectedIndex = 1 Then
            comPort.Parity = Parity.Odd
        Else
            comPort.Parity = Parity.Even
        End If
        If cmbStopBit.SelectedIndex = 0 Then
            comPort.StopBits = StopBits.One
        Else
            comPort.StopBits = StopBits.Two
        End If

        comPort.Open()

        slave = ModbusSerialSlave.CreateRtu(slaveID, comPort)
        AddHandler slave.ModbusSlaveRequestReceived, AddressOf Modbue_Request_Event
        slave.DataStore = Modbus.Data.DataStoreFactory.CreateDefaultDataStore()
        AddHandler slave.DataStore.DataStoreWrittenTo, AddressOf Modbus_DataStoreWriteTo
        slave.Listen()
        btOpenCOM.Enabled = False
        btCloseCOM.Enabled = True
        Timer1.Enabled = True
    End Sub

    Private Sub btCloseCOM_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btCloseCOM.Click
        'stop RTU slave
        Timer1.Enabled = False
        comPort.Close()
        slave.Stop()
        slave.Dispose()
        btOpenCOM.Enabled = True
        btCloseCOM.Enabled = False
    End Sub

    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick
        'update input values to DataStore
        'DO
        slave.DataStore.CoilDiscretes(1) = chkDO1.Checked
        slave.DataStore.CoilDiscretes(2) = chkDO2.Checked
        slave.DataStore.CoilDiscretes(3) = chkDO3.Checked
        slave.DataStore.CoilDiscretes(4) = chkDO4.Checked
        'DI
        slave.DataStore.InputDiscretes(1) = chkDI1.Checked
        slave.DataStore.InputDiscretes(2) = chkDI2.Checked
        slave.DataStore.InputDiscretes(3) = chkDI3.Checked
        slave.DataStore.InputDiscretes(4) = chkDI4.Checked
        'AO
        slave.DataStore.HoldingRegisters(1) = Convert.ToUInt16(txtAO1.Text)
        slave.DataStore.HoldingRegisters(2) = Convert.ToUInt16(txtAO2.Text)
        slave.DataStore.HoldingRegisters(3) = Convert.ToUInt16(txtAO3.Text)
        slave.DataStore.HoldingRegisters(4) = Convert.ToUInt16(txtAO4.Text)
        'AI
        slave.DataStore.InputRegisters(1) = Convert.ToUInt16(txtAI1.Text)
        slave.DataStore.InputRegisters(2) = Convert.ToUInt16(txtAI2.Text)
        slave.DataStore.InputRegisters(3) = Convert.ToUInt16(txtAI3.Text)
        slave.DataStore.InputRegisters(4) = Convert.ToUInt16(txtAI4.Text)
    End Sub
End Class
