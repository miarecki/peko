Sub Munchhausen()

    Dim kNum As Long, Num As Long
    Dim Limit As Long
    Dim Digit As Long, i As Byte
    Dim DigitPower As Long, Sum As Long
    Dim Counter As Byte
    Dim NumStr As String, Msg As String
    Dim CzyZera As Integer
    
    kNum = InputBox(" Wpisz maksymalna ilosc cyfr: ")
    CzyZera = MsgBox("Czy 0^0 = 0?", vbYesNo)
    Limit = (10 ^ kNum) - 1
    
    For Num = 0 To Limit
        NumStr = CStr(Num)
    For i = 1 To Len(NumStr)
        Digit = Mid(NumStr, i, 1)
        If Digit > 0 Then
        DigitPower = Digit ^ Digit
        Sum = Sum + DigitPower
        Else
            Sum = Sum + 1
        End If
        Next i
    If Num = Sum And Len(CStr(Num)) = kNum Then
        Msg = Msg & Num & ", "
        Counter = Counter + 1
    End If
    Sum = 0
    Next Num
    
    Select Case Counter
        Case 0
        MsgBox " Nie ma " & kNum & "-cyfrowych takich liczb."
    
    Case Is > 0
        Msg = Left(Msg, Len(Msg) - 2)
        MsgBox " Jest " & Counter & " " & kNum _
        & "-cyfrowych takich liczb : " & Msg & "."
    
    End Select

End Sub
