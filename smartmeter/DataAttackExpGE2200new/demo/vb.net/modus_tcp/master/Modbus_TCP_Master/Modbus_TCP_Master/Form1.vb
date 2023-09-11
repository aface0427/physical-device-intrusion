Imports System
Imports System.Collections.Generic
Imports System.Text
'step1. reference nmodbuspc.dll, and using the namespaces.
Imports Modbus.Device      'for modbus master
Imports System.Net         'for tcp client
Imports System.Net.Sockets
Imports System.Runtime.InteropServices

Public Class Form1
    Inherits System.Windows.Forms.Form
    Public Declare Function InternetGetConnectedState Lib "wininet" (ByRef dwFlags As Long, ByVal dwReserved As Long) As Boolean

    Private tcpClient As TcpClient
    Private master As ModbusIpMaster
    Private ipAddress As String
    Private tcpPort As Integer = 502
    Private dtDisconnect As New DateTime()
    Private dtNow As New DateTime()

    Private listDI As New List(Of PictureBox)
    Private listDO As New List(Of PictureBox)
    Private listAI As New List(Of TextBox)
    Private listAO As New List(Of TextBox)

    Private NetworkIsOK = False

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        listDI.Add(DI0)
        listDI.Add(DI1)
        listDI.Add(DI2)
        listDI.Add(DI3)

        listDO.Add(DO0)
        listDO.Add(DO1)
        listDO.Add(DO2)
        listDO.Add(DO3)

        listAI.Add(AI0)
        listAI.Add(AI1)
        listAI.Add(AI2)
        listAI.Add(AI3)

        listAO.Add(AO0)
        listAO.Add(AO1)
        listAO.Add(AO2)
        listAO.Add(AO3)
        dtDisconnect = DateTime.Now
    End Sub

    Private Sub btnStart_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnStart.Click
        NetworkIsOK = connect()
        Timer1.Interval = 1000
        Timer1.Enabled = True
        btnStart.Enabled = False
        btnStop.Enabled = True
    End Sub

    Private Sub btnStop_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnStop.Click
        Timer1.Enabled = False
        If Not (master Is Nothing) Then
            master.Dispose()
        End If
        If Not (tcpClient Is Nothing) Then
            tcpClient.Close()
        End If
        Me.Text = "Off line " + DateTime.Now.ToString()
        btnStart.Enabled = True
        btnStop.Enabled = False
    End Sub

    Private Function connect() As Boolean
        ipAddress = txtIP.Text
        If Not (master Is Nothing) Then
            master.Dispose()
        End If
        If Not (tcpClient Is Nothing) Then
            tcpClient.Close()
        End If
        If CheckInternet() = True Then
            Try
                'connect to Modbus TCP Server

                tcpClient = New TcpClient()
                Dim asyncResult As IAsyncResult = tcpClient.BeginConnect(ipAddress, tcpPort, Nothing, Nothing)
                asyncResult.AsyncWaitHandle.WaitOne(300, True) 'wait for 3 sec
                If asyncResult.IsCompleted = False Then
                    tcpClient.Close()
                    Console.WriteLine(DateTime.Now.ToString() + ":Cannot connect to server.")
                    Return False
                End If

                'tcpClient = New TcpClient(ipAddress, tcpPort)
                'create Modbus TCP Master by the tcp client
                master = ModbusIpMaster.CreateIp(tcpClient)
                master.Transport.Retries = 0
                master.Transport.ReadTimeout = 1500 'millionsecs
                Me.Text = "On line " + DateTime.Now.ToString()
                Console.WriteLine(DateTime.Now.ToString() + ":Connect to server.")
                Return True
            Catch ex As Exception
                Console.WriteLine(DateTime.Now.ToString() + ":Connect process " + ex.StackTrace + "==>" + ex.Message)
                Return False
            End Try
        End If
        Return False
    End Function

    Private Function CheckInternet() As Boolean
        'http://msdn.microsoft.com/en-us/library/windows/desktop/aa384702(v=vs.85).aspx
        Dim INTERNET_CONNECTION_LAN As Long = 2
        Return InternetGetConnectedState(INTERNET_CONNECTION_LAN, 0)
    End Function

    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick
        Try
            If NetworkIsOK = True Then
                Dim slaveID As Byte = 1
                Dim startAddress As UShort = 0
                Dim numofPoints As UShort = 4
                'read DI(1xxxx)
                Dim status() As Boolean = master.ReadInputs(slaveID, startAddress, numofPoints)
                For i As Integer = 0 To numofPoints - 1
                    If status(i) = True Then
                        listDI(i).BackColor = Color.Lime
                    Else
                        listDI(i).BackColor = Color.Green
                    End If
                Next
                'read DO(0xxxx)
                Dim coils() As Boolean = master.ReadCoils(slaveID, startAddress, numofPoints)
                For i As Integer = 0 To numofPoints - 1
                    If coils(i) = True Then
                        listDO(i).BackColor = Color.Red
                    Else
                        listDO(i).BackColor = Color.Maroon
                    End If
                Next
                'read AI(3xxxx)
                Dim register() As UShort = master.ReadInputRegisters(slaveID, startAddress, numofPoints)
                For i As Integer = 0 To numofPoints - 1
                    'If you need to show the value with other unit, you have to caculate the gain and offset
                    'eq. 0 to 0kg, 32767 to 1000kg
                    '0 (kg) = gain * 0 + offset
                    '1000 (kg) = gain *32767 + offset
                    '=> gain=1000/32767, offset=0
                    'Dim value As Double = CDbl(register(i) * 1000.0 / 32767)
                    'listAI(i).Text = value.ToString("0.00")
                    listAI(i).Text = register(i).ToString()
                Next
                'read AO(4xxxx)
                Dim holding_register() As UShort = master.ReadHoldingRegisters(slaveID, startAddress, numofPoints)
                For i As Integer = 0 To numofPoints - 1
                    'If you need to show the value with other unit, you have to caculate the gain and offset
                    'eq. 0 to 0 mA, 32767 to 20 mA
                    '0 (mA) = gain * 0 + offset
                    '20 (mA) = gain *32767 + offset
                    '=> gain=20/32767, offset=0
                    'Dim value As Double = CDbl(holding_register(i) * 20.0 / 32767)
                    'listAO(i).Text = value.ToString("0.00")
                    listAO(i).Text = holding_register(i).ToString()
                Next
            Else
                dtNow = DateTime.Now
                If (dtNow - dtDisconnect) > TimeSpan.FromSeconds(10) Then
                    Console.WriteLine(DateTime.Now.ToString() + ":Start connecting")
                    NetworkIsOK = connect()
                    If NetworkIsOK = False Then
                        Console.WriteLine(DateTime.Now.ToString() + ":Connecting fail. Wait for retry")
                        dtDisconnect = DateTime.Now
                    End If
                Else
                    Console.WriteLine(DateTime.Now.ToString() + ":Wait for retry connecting")
                End If
            End If
        Catch ex As Exception
            'Connection exception
            'No response from server.
            'The server maybe close the connection, or response timeout.
            If ex.Source.Equals("System") Then
                NetworkIsOK = False
                Console.WriteLine(DateTime.Now + " " + ex.Message)
                Me.Text = "Off line " + DateTime.Now.ToString()
                dtDisconnect = DateTime.Now
            End If
            'The server return error code.
            'You can get the function code and exception code.
            If ex.Source.Equals("nModbuPC") Then
                Dim str As String = ex.Message
                Dim funcode As Integer
                Dim expcode As String

                str = str.Remove(0, str.IndexOf("\r\n" + 17))
                funcode = Convert.ToInt16(str.Remove(str.IndexOf("\r\n")))
                Console.WriteLine("Function code: " + funcode.ToString("X"))

                str = str.Remove(0, str.IndexOf("\r\n" + 17))
                expcode = str.Remove(str.IndexOf("-"))
                Select Case expcode.Trim()
                    Case "1"
                        Console.WriteLine("Exception Code: " + expcode.Trim() + "----> Illegal function!")
                        Exit Select
                    Case "2"
                        Console.WriteLine("Exception Code: " + expcode.Trim() + "----> Illegal data address!")
                        Exit Select
                    Case "3"
                        Console.WriteLine("Exception Code: " + expcode.Trim() + "----> Illegal data value!")
                        Exit Select
                    Case "4"
                        Console.WriteLine("Exception Code: " + expcode.Trim() + "----> Slave device failure!")
                        Exit Select
                End Select
                'Modbus exception codes definition 

                '                       * Code   * Name                                      * Meaning
                '                         01       ILLEGAL FUNCTION                            The function code received in the query is not an allowable action for the server.

                '                         02       ILLEGAL DATA ADDRESS                        The data addrdss received in the query is not an allowable address for the server.

                '                         03       ILLEGAL DATA VALUE                          A value contained in the query data field is not an allowable value for the server.

                '                         04       SLAVE DEVICE FAILURE                        An unrecoverable error occurred while the server attempting to perform the requested action.

                '                         05       ACKNOWLEDGE                                 This response is returned to prevent a timeout error from occurring in the client (or master)
                '                                                                              when the server (or slave) needs a long duration of time to process accepted request.

                '                         06       SLAVE DEVICE BUSY                           The server (or slave) is engaged in processing a long¡Vduration program command , and the
                '                                                                              client (or master) should retransmit the message later when the server (or slave) is free.

                '                         08       MEMORY PARITY ERROR                         The server (or slave) attempted to read record file, but detected a parity error in the memory.

                '                         0A       GATEWAY PATH UNAVAILABLE                    The gateway is misconfigured or overloaded.

                '                         0B       GATEWAY TARGET DEVICE FAILED TO RESPOND     No response was obtained from the target device. Usually means that the device is not present on the network.
            End If
        End Try
    End Sub

    'set DO
    Private Sub DO_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles DO0.Click, DO3.Click, DO2.Click, DO1.Click
        Dim slaveID As Byte = 1
        If NetworkIsOK = True Then
            Dim pic As PictureBox = CType(sender, PictureBox)
            Dim index As UShort = UShort.Parse(pic.Tag.ToString())
            If pic.BackColor = Color.Maroon Then
                master.WriteSingleCoil(slaveID, index, True)
            Else
                master.WriteSingleCoil(slaveID, index, False)
            End If
        End If
    End Sub

    'set AO
    Private Sub AO_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles AO0.Click, AO3.Click, AO1.Click, AO2.Click
        Dim slaveID As Byte = 1
        Dim txt As TextBox = CType(sender, TextBox)
        Dim inputvalue As New frmInputValue()
        If NetworkIsOK = True Then
            Dim index As UShort = UShort.Parse(txt.Tag.ToString())
            inputvalue.StringValue = txt.Text
            inputvalue.ShowDialog()
            If inputvalue.DialogResult = Windows.Forms.DialogResult.OK Then
                Dim value As Double = inputvalue.Value
                Dim aovalue As UShort = CUShort(value)

                'use gain=20/32767, offset=0
                'Dim aovalue As UShort = CUShort(value * 32767 / 20.0)
                master.WriteSingleRegister(slaveID, index, aovalue)
            End If
        End If
    End Sub
End Class
