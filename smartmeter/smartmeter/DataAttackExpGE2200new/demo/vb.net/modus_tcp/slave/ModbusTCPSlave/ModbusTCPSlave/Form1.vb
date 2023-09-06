Imports System
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Drawing
Imports System.Text
Imports System.Windows.Forms
Imports Modbus
Imports Modbus.Device
Imports Modbus.Data
Imports System.Net
Imports System.Net.Sockets
Imports System.Threading

Public Class Form1
    Private slave As ModbusSlave
    Dim slaveTcpListener As TcpListener
    Private slaveID As Byte = 1
    Private port As Integer = 502

    Private Sub Modbus_Request_Event(ByVal sender As Object, ByVal e As Modbus.Device.ModbusSlaveRequestEventArgs)
        'request from master
        Dim fc As Byte = e.Message.FunctionCode
        Dim data() As Byte = e.Message.MessageFrame
        Dim byteStartaddress() As Byte = {data(3), data(2)}
        Dim byteNum() As Byte = {data(5), data(4)}
        Dim startAddress As Short = BitConverter.ToInt16(byteStartaddress, 0)
        Dim NumOfPoint As Short = BitConverter.ToInt16(byteNum, 0)
        Console.WriteLine(fc.ToString() + "," + startAddress.ToString() + "," + NumOfPoint.ToString())
    End Sub
#Region "Set AO"
    Private Delegate Sub UpdateAOStatusDelegate(ByVal index As Integer, ByVal message As String)
    Private Sub DoAOUpdate(ByVal index As Integer, ByVal message As String)
        If Me.InvokeRequired Then
            ' we were called on a worker thread
            ' marshal the call to the user interface thread
            Me.Invoke(New UpdateAOStatusDelegate(AddressOf DoAOUpdate), New Object() {index, message})
            Return
        End If

        ' this code can only be reached
        ' by the user interface thread
        Select Case index
            Case 0
                Me.txtAO1.Text = message
            Case 1
                Me.txtAO2.Text = message
            Case 2
                Me.txtAO3.Text = message
            Case 3
                Me.txtAO4.Text = message
        End Select

    End Sub
#End Region

#Region "Set DO"
    Private Delegate Sub UpdateDOStatusDelegate(ByVal index As Integer, ByVal value As Boolean)
    Private Sub DoDOUpdate(ByVal index As Integer, ByVal value As Boolean)
        If Me.InvokeRequired Then
            ' we were called on a worker thread
            ' marshal the call to the user interface thread
            Me.Invoke(New UpdateDOStatusDelegate(AddressOf DoDOUpdate), New Object() {index, value})
            Return
        End If

        ' this code can only be reached
        ' by the user interface thread
        Select Case index
            Case 0
                Me.chkDO1.Checked = value
            Case 1
                Me.chkDO2.Checked = value
            Case 2
                Me.chkDO3.Checked = value
            Case 3
                Me.chkDO4.Checked = value
        End Select

    End Sub
#End Region
    Private Sub Modbus_DataStoreWriteTo(ByVal sender As Object, ByVal e As Modbus.Data.DataStoreEventArgs)
        'this.Text = "DataType=" + e.ModbusDataType.ToString() + "  StartAdress=" + e.StartAddress;
        Dim iAddress As Integer = e.StartAddress 'e.StartAddress;
        Select Case e.ModbusDataType
            Case ModbusDataType.HoldingRegister
                For i As Integer = 0 To e.Data.B.Count - 1
                    'Set AO                 

                    'e.Data.B(i) already write to slave.DataStore.HoldingRegisters(e.StartAddress + i + 1)
                    'e.StartAddress starts from 0
                    'You can set AO value to hardware here
                    DoAOUpdate(iAddress, e.Data.B(i).ToString())
                    iAddress += 1
                    If e.Data.B.Count = 1 Then
                        Exit For
                    End If
                Next i

            Case ModbusDataType.Coil
                For i As Integer = 0 To e.Data.A.Count - 1
                    'Set DO

                    'e.Data.A(i) already write to slave.DataStore.CoilDiscretes(e.StartAddress + i + 1)
                    'e.StartAddress starts from 0
                    'You can set DO value to hardware here
                    DoDOUpdate(iAddress, e.Data.A(i))
                    iAddress += 1
                    If e.Data.A.Count = 1 Then
                        Exit For
                    End If
                Next i
        End Select
    End Sub

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        'Dim addr As System.Net.IPAddress
        'addr = New System.Net.IPAddress(Dns.GetHostEntry(Dns.GetHostName()).AddressList(0).Address)
        Dim ipEntry As IPHostEntry = Dns.GetHostEntry(Dns.GetHostName())
        Dim addr() As IPAddress = ipEntry.AddressList
        labServerName.Text = "Host IP=" & addr(0).ToString()
    End Sub


    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick
        'update input values to datastore
        'DI
        slave.DataStore.InputDiscretes(1) = chkDI1.Checked
        slave.DataStore.InputDiscretes(2) = chkDI2.Checked
        slave.DataStore.InputDiscretes(3) = chkDI3.Checked
        slave.DataStore.InputDiscretes(4) = chkDI4.Checked
        'AI
        slave.DataStore.InputRegisters(1) = Convert.ToUInt16(txtAI1.Text)
        slave.DataStore.InputRegisters(2) = Convert.ToUInt16(txtAI2.Text)
        slave.DataStore.InputRegisters(3) = Convert.ToUInt16(txtAI3.Text)
        slave.DataStore.InputRegisters(4) = Convert.ToUInt16(txtAI4.Text)
        'AO
        slave.DataStore.HoldingRegisters(1) = Convert.ToUInt16(txtAO1.Text)
        slave.DataStore.HoldingRegisters(2) = Convert.ToUInt16(txtAO2.Text)
        slave.DataStore.HoldingRegisters(3) = Convert.ToUInt16(txtAO3.Text)
        slave.DataStore.HoldingRegisters(4) = Convert.ToUInt16(txtAO4.Text)
        'DO
        slave.DataStore.CoilDiscretes(1) = chkDO1.Checked
        slave.DataStore.CoilDiscretes(2) = chkDO2.Checked
        slave.DataStore.CoilDiscretes(3) = chkDO3.Checked
        slave.DataStore.CoilDiscretes(4) = chkDO4.Checked
    End Sub


    Private Sub btnStart_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnStart.Click
        ' create and start the TCP slave
        'Dim ipEntry As IPHostEntry = Dns.GetHostEntry(Dns.GetHostName())
        'Dim addr() As IPAddress = ipEntry.AddressList
        Dim addr As IPAddress = IPAddress.Parse("127.0.0.1")
        For Each ip As IPAddress In Dns.GetHostEntry(Dns.GetHostName()).AddressList
            If ip.AddressFamily = AddressFamily.InterNetwork Then
                addr = ip
                Exit For
            End If

        Next
        slaveTcpListener = New TcpListener(addr, port)
        slaveTcpListener.Start()

        slave = Modbus.Device.ModbusTcpSlave.CreateTcp(slaveID, slaveTcpListener)
        AddHandler slave.ModbusSlaveRequestReceived, AddressOf Modbus_Request_Event
        slave.DataStore = Modbus.Data.DataStoreFactory.CreateDefaultDataStore()
        AddHandler slave.DataStore.DataStoreWrittenTo, AddressOf Modbus_DataStoreWriteTo
        slave.Listen()

        Timer1.Enabled = True
        btnStart.Enabled = False
        btnStop.Enabled = True
    End Sub

    Private Sub btnStop_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnStop.Click
        Timer1.Enabled = False
        btnStart.Enabled = True
        btnStop.Enabled = False
        slave.Stop()
        slave.Dispose()
        slaveTcpListener.Stop()
        'Me.Close()
    End Sub
End Class
