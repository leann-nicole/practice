.model small
.stack 100h
data segment
	prompt1 db 'Enter string: $'
	result db 'C count: $'
	newline db 10,13,'$'
	message db 50
			db ?
			db 50 dup('$')
	ccount db '$$$'							; c count in string format
data ends
code segment
	assume ds:data, cs:code
	start:
		mov ax, data
		mov ds, ax
		
		lea si, message						; address to start writing string
		
		lea dx, prompt1						; say 'Enter string: '
		mov ah, 09h
		int 21h

		mov dx, si							; get user string input
		mov ah, 0ah
		int 21h

		lea dx, newline 					; add a newline
		mov ah, 09h
		int 21h

		lea dx, result 						; say 'C count: '
		mov ah, 09h
		int 21h
		
		mov bx, 0000h						; here we store the c count	
		add si, 1							; we don't want the metadata

		evaluate:
			inc si							; next character
			cmp byte ptr[si], '$'			; terminating character, string completely evaluated
			je present_count
			cmp byte ptr[si], 'c'			; a letter c!
			jne evaluate
			add bx, 1						; so we add 1 to the count
			jmp evaluate

		present_count:	

			mov ax, bx						; mov to ax, since ax will be used in division
			lea si, ccount					; point to the location for number string
			call num2string					; convert			
	
			lea dx, ccount					; point where to 09h will start reading
			mov ah, 09h
			int 21h		

		mov ah, 4ch							; return control to DOS
		int 21h
;------------------------------NUM2STRING BORROWED FROM PROGRAM 2------------------------------------
	num2string proc
		mov bx, 0ah					; continuous div by 10 will extract each digit
		mov cx, 0					; to count how many digits, useful in popping from TOS

		extract:
			mov dx, 0				; reset the previous remainder
			div bx					; dx/bx : dx = remainder, ax = quotient
			push dx					; push the remainder (dx) on TOS
			inc cx
			cmp ax, 0				; if quotient is zero, we have extracted all the digits, proceed to form
			jne extract				; else do extraction again

		form:
			pop dx					; get value from TOS
			add dl, '0'				; convert it to ASCII representation to be able to print
			mov [si], dl			; replacing the dollar signs in numstring with the digit
			inc si
			loop form

		ret
	num2string endp
code ends
end start