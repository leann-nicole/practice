.model small
.stack 100h
data segment 
	prompt1 db "Lowercase letter: $"
	prompt2 db 10,13,"Uppercase version: $"
data ends
code segment
	assume ds:data, cs:code
	start:
		mov ax, data				; initialize the data segment
		mov ds, ax

		lea dx, prompt1				; print prompt1, ask for user input
		mov ah, 09h
		int 21h		
		
		mov ah, 01h					; receive user input
		int 21h

		lea dx, prompt2				; print prompt2
		mov ah, 09h
		int 21h		
	
		mov dl,al					; user input is stored in al, move it to dl in order to display
	
		sub dl, 32					; ASCII: a = 97, A = 65
		mov ah, 02h
		int 21h

		mov ah, 4ch					; return control to DOS
		int 21h	
code ends
end start