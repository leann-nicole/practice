.model small
.stack 100h
data segment
	prompt1 db 'Enter decimal number: $'
	prompt2 db 'Octal version: $'
	newline db 10,13,'$'
	deci db '$$$$$$$$$$'						; hold string version of user-given decimal number
	octa db '$$$$$$$$$$'						; hold string version of its octal equivalent
	multiple dw 10								; for converting string deci to value
	value dw 0 									; variable to store actual value of deci
data ends
code segment
	assume ds:data, cs:code
	main proc
		mov ax, data
		mov ds, ax

		lea si, deci
		lea di, value

		lea dx, prompt1							; say 'Enter decimal number: '
		mov ah, 09h
		int 21h

		mov dx, si								; take user input, store in deci offset
		mov ah, 0ah
		int 21h

		call string2num 						; convert user-given number string to actual number, store in value offset

		lea si, octa
		mov ax, value							; since we'll repeatedly divide value by 8 to convert to octal
		call num2string

		lea dx, newline							; print a newline
		mov ah, 09h
		int 21h

		lea dx, prompt2							; say 'Octal version: '
		mov ah, 09h
		int 21h

		lea dx, octa							; the octal number!
		mov ah, 09h
		int 21h

		mov ah, 4ch								; return control to DOS
		int 21h
	main endp
;------------------------STRING2NUM FROM PROGRAM7-----------------------------------------------
	string2num proc
		inc si									; look at number of digits entered
		mov cl, [si]							; used for traversing the number (loop)
		mov ch, 0								; let cx == cl
		add si, cx								; si now points to LSD <----
		
		mov bx, 1								; will hold multiples of 10 

		calculate:
			mov al, [si]						; current char to process
			sub al, 48							; from ASCII to numeric value
			mov ah, 0							; clear results from prev calculation
												
			mul bx								; since ax = ax * bx
			add [di], ax
		
			mov ax, bx
			mul multiple						; 1, 10, 100, 1000...
			mov bx, ax							; new multiple of 10

			dec si								; process next char to convert 2 digit
			loop calculate
		
		ret
	string2num endp
;--------------------------NUM2STRING FROM PROGRAM2-----------------------------------------------
	num2string proc
		mov bx, 08h					; continuous div by 8 will extract each digit
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
end main