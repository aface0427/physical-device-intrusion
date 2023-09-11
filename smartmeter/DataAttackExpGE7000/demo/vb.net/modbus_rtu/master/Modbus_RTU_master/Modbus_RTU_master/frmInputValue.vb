Imports System
Imports System.Collections.Generic
Imports System.ComponentModel
Imports System.Data
Imports System.Drawing
Imports System.Text

Public Class frmInputValue
    Inherits System.Windows.Forms.Form
    Public Property Value() As Double
        Set(ByVal value As Double)
            Me.txtValue.Text = value
        End Set
        Get
            Return Me.txtValue.Text
        End Get
    End Property
    Public Property StringValue() As String
        Set(ByVal value As String)
            Me.txtValue.Text = value
        End Set
        Get
            Return Me.txtValue.Text
        End Get
    End Property
    Private Function Convert_To_Double(ByVal sKey As String) As Double
        If sKey = "" Then
            sKey = "0"
        End If
        Return Double.Parse(sKey)
    End Function


    Private Sub Number_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles Button1.Click, _
        Button9.Click, Button8.Click, Button7.Click, Button6.Click, Button5.Click, Button4.Click, Button3.Click, Button2.Click, Button10.Click

        Dim index As Button = CType(sender, Button)
        txtValue.Text = txtValue.Text + index.Tag.ToString()
    End Sub

    Private Sub btncommon_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles btncommon.Click
        If txtValue.Text.IndexOf(".") < 0 Then
            txtValue.Text += "."
        End If
    End Sub

    Private Sub btndel_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles btndel.Click
        txtValue.Text = txtValue.Text.Substring(0, txtValue.Text.Length - 1)
    End Sub

    Private Sub btClr_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles btClr.Click
        txtValue.Text = ""
    End Sub

    Private Sub btMinus_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles btMinus.Click
        If Convert_To_Double(txtValue.Text) > 0 Then
            txtValue.Text = (Convert_To_Double(txtValue.Text) * (-1)).ToString()
        End If
    End Sub

    Private Sub btPlus_Click(ByVal sender As Object, ByVal e As System.EventArgs) Handles btPlus.Click
        If Convert_To_Double(txtValue.Text) < 0 Then
            txtValue.Text = (Convert_To_Double(txtValue.Text) * (-1)).ToString()
        End If
    End Sub
End Class



