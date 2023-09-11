Imports System
Imports System.Collections.Generic
Imports System.Text
'step1. reference nmodbuspc.dll, and using the namespaces.
Imports Modbus.Device      'for modbus master
Imports System.IO.Ports    'for controlling serial ports


Public Class Form1
    Inherits System.Windows.Forms.Form
    Private serialPort As New SerialPort()   'declare object and create a new SerialPort object with default settings.
    Private master As ModbusSerialMaster

    Private listAI As New List(Of TextBox)
    Private listAO As New List(Of TextBox)
    Private listDI As New List(Of PictureBox)
    Private listDO As New List(Of PictureBox)

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        cmbcom.SelectedIndex = 2
        cmbbaud.SelectedIndex = 0
        cmbdb.SelectedIndex = 0
        cmbpty.SelectedIndex = 0
        cmbsb.SelectedIndex = 0

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
        btnOpen.Enabled = True
        btnClose.Enabled = False

    End Sub
    'open port 
    Private Sub btnOpen_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnOpen.Click

        'get port properties
        serialPort.PortName = cmbcom.SelectedItem.ToString()
        serialPort.BaudRate = Integer.Parse(cmbbaud.SelectedItem.ToString())
        serialPort.DataBits = Integer.Parse(cmbdb.SelectedItem.ToString())
        'get parity 
        If cmbpty.SelectedIndex = 0 Then
            serialPort.Parity = Parity.None
        ElseIf cmbpty.SelectedIndex = 1 Then
            serialPort.Parity = Parity.Even
        Else
            serialPort.Parity = Parity.Odd
        End If
        'get stop bit
        If cmbsb.SelectedIndex = 0 Then
            serialPort.StopBits = StopBits.One
        Else
            serialPort.StopBits = StopBits.Two
        End If

        Try
            serialPort.Open()
            'create Modbus RTU Master by the comport client
            master = ModbusSerialMaster.CreateRtu(serialPort)
            master.Transport.Retries = 0
            master.Transport.ReadTimeout = 300  'millionsecs
            btnOpen.Enabled = False
            btnClose.Enabled = True
            Timer1.Enabled = True
            Console.WriteLine(DateTime.Now + "=>Open " + serialPort.PortName + " successfully.")
        Catch ex As Exception
            Console.WriteLine("Error:" + ex.Message)
        End Try
    End Sub
    'close port
    Private Sub btnClose_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnClose.Click
        Timer1.Enabled = False
        serialPort.Close()
        btnOpen.Enabled = True
        btnClose.Enabled = False
        Console.WriteLine(DateTime.Now + "=>Disconnect " + serialPort.PortName)
    End Sub

    Private Sub Timer1_Tick(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Timer1.Tick
        Dim slaveID As Byte = 1
        Dim startAddress As UShort = 0
        Dim numOfPoints As UShort = 4

        Try
            'read DI(1xxxx)
            Dim status() As Boolean = master.ReadInputs(slaveID, startAddress, numOfPoints)
            For i As Integer = 0 To numOfPoints - 1
                If status(i) = True Then
                    listDI(i).BackColor = Color.DodgerBlue
                Else
                    listDI(i).BackColor = Color.Navy
                End If
            Next
            'read DO(0xxxx)
            Dim coils() As Boolean = master.ReadCoils(slaveID, startAddress, numOfPoints)
            For i As Integer = 0 To numOfPoints - 1
                If coils(i) = True Then
                    listDO(i).BackColor = Color.Red
                Else
                    listDO(i).BackColor = Color.DarkRed
                End If
            Next
            'read AI(3xxxx)
            Dim register() As UShort = master.ReadInputRegisters(slaveID, startAddress, numOfPoints)
            For i As Integer = 0 To numOfPoints - 1
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
            Dim holding_register() As UShort = master.ReadHoldingRegisters(slaveID, startAddress, numOfPoints)
            For i As Integer = 0 To numOfPoints - 1
                'If you need to show the value with other unit, you have to caculate the gain and offset
                'eq. 0 to 0 mA, 32767 to 20 mA
                '0 (mA) = gain * 0 + offset
                '20 (mA) = gain *32767 + offset
                '=> gain=20/32767, offset=0
                'Dim value As Double = CDbl(holding_register(i) * 20.0 / 32767)
                'listAO(i).Text = value.ToString("0.00")
                listAO(i).Text = holding_register(i).ToString()
            Next
        Catch ex As Exception
            'Connection exception
            'No response from server.
            'The server maybe close the connection, or response timeout.
            If ex.Source.Equals("System") Then
                Console.WriteLine(DateTime.Now + " " + ex.Message)
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
    'set do
    Private Sub DO_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles DO0.Click, DO3.Click, DO2.Click, DO1.Click
        Dim slaveID As Integer = 1
        If serialPort.IsOpen = True Then
            Dim pic As PictureBox = CType(sender, PictureBox)
            Dim index As UShort = UShort.Parse(pic.Tag.ToString())
            If pic.BackColor = Color.DarkRed Then
                master.WriteSingleCoil(slaveID, index, True)
            Else
                master.WriteSingleCoil(slaveID, index, False)
            End If
        End If
    End Sub
    'set ao
    Private Sub AO_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles AO0.Click, AO3.Click, AO2.Click, AO1.Click
        Dim slaveID As Integer = 1
        Dim txt As TextBox = CType(sender, TextBox)
        Dim inputvalue As New frmInputValue()
        If serialPort.IsOpen = True Then
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
