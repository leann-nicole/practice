.model small
.stack 100h
.data
	num dw 0						; start from 0
	whitespace db ' $'
	numstring db '$$$'				; 0-99 but in string format
.code
	main proc
		mov ax, @data
		mov ds, ax

		start:		
			cmp num, 100
			jne print				; if not num != 100, print it
			jmp terminate			; else end program

		print:	
			lea si, numstring		; source index = offset of numstring in data segment
			mov ax, num				; ax will be divided in the num2string procedure
			call num2string			; convert num to string, able to display greater than 9
		
			lea dx, numstring 		; number is now in string with dollar sign terminator
			mov ah, 09h				; display up until dollar sign
			int 21h			

			lea dx, whitespace		; next digit will print below current digit
			mov ah, 09h
			int 21h

			inc num					; num++ will equal 100 eventually
			jmp start				; repeat

		terminate:
			mov ax, 4c00h			; return control to DOS
			int 21h
			main endp

	num2string proc
		call dollarfiller			; reset, else digits from previous number might be printed
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

	dollarfiller proc
		mov cx, 3					; for the loop, since we have 3 characters to fill
		lea di, numstring			; load the offset of numstring to destination index
		mov bl, '$'
		dollarloop:					; loop will terminate when count register == 0
			mov [di], bl
			inc di
			loop dollarloop
		
		ret
	dollarfiller endp
end main