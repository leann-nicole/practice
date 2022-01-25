.model small
.stack 100h
say macro text
	lea dx, text							
	mov ah, 09h							
	int 21h
endm
data segment 
	prompt1 db 'Enter string: $'
	prompt2 db 'Reversed: $'
	message db 50 dup('$')							; a string of 50 dollar signs
	strrev db 50 dup('$')								
	newline db 10,13,'$'					
data ends
code segment
	assume ds:data, cs:code
	start:
		mov ax, data
		mov ds, ax

		lea si, message								; where we start writing user's string
		lea di, strrev								; where we start writing its reverse

		say prompt1									; say macro expansion, say 'Enter string:'

		mov dx, si									; user inputs string
		mov ah, 0ah									; getline
		int 21h

		mov bx, 0000h								; bx will hold the charcount

		add si, 2									; don't count the metadata (size and actual size)
		countchar:
			mov al, [si]
			inc si
			inc bx
			cmp al, '$'
			jne countchar

		sub si, 3									; because there are 2 dollar signs and a newline char
		sub bx, 2									; because bx is a step behind si so just subtract 2
		mov cx, bx									; count = number of characters, used in reverse loop		

		reverse:
			mov al, [si]							; use al not ax since [si] and [di] use bytes not words
			mov [di], al
			dec si
			inc di
			loop reverse

		say newline									; reversed string prints below orig string

		say prompt2									; say 'Reversed:'

		say strrev									; the reversed string

		mov ah, 4ch									; return control to DOS
		int 21h
		
code ends
end start