.model small
.stack 100h
data segment 
    members db 'We are Group 4.',10,10,13
           db ' Adrian Francis Arquiza',10,13
           db ' Allan Duran',10,13 
           db ' Jan Clark Dayucos',10,13
           db ' Jay Baldezamo',10,13
           db ' Leann Nicole Velasco',10,13
           db ' Lezyl Pearl Cueco',10,13
           db ' Maureen Ortiz$'
data ends
code segment
    assume ds:data, cs:code       
    start:
        mov ax, data   						; initialize data segment
        mov ds, ax 
        
        lea dx, members 					; or mov dx, offset myname   
        mov ah, 09h    						; 09h outputs up until dollar sign($)
        int 21h
            
       mov ah, 4ch     						; 4ch gives control back to DOS
       int 21h 
code ends          
end start