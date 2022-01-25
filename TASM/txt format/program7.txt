.model small
.stack 100h
ask macro text, offs
	lea dx, text								; display prompt asking for input
	mov ah, 09h
	int 21h
	
	mov dx, offs								; receive string input and store in offset
	mov ah, 0ah
	int 21h

	lea dx, newline								; newline
	mov ah, 09h
	int 21h
endm
show_result macro operation
	lea dx, newline
	mov ah, 09h
	int 21h

	lea dx, operation							; display operation used to get answer
	mov ah, 09h
	int 21h

	lea dx, answer								; display the answer
	mov ah, 09h
	int 21h

	mov ax, 0									; reset and prepare registers for next operation
	mov bx, 0									; values in val1 and val2 are retained
	mov cx, 0
	mov dx, 0

endm
data segment
	prompt1 db 'First number: $'
	prompt2 db 'Second number: $'
	num1 db 4									; max digits is 3 + newline char
		 db ?									; holds actual num of digits entered
		 db 5 dup('$')							; including newline char
	num2 db 4									
		 db ?									
		 db 5 dup('$')
	val1 dw 0									; numeric value of num1
	val2 dw 0									; numeric value of num2
	multiple dw 10								; used in deriving numeric value from string of digit chars
	newline db 10,13,'$'
	answer db '$$$$$$$'							; will hold answer, in printable string form
	op1 db 'Addition: $'
	op2 db 'Subtraction: $'
	op3 db 'Divide: $'
	op4 db 'Multiply: $'
data ends
code segment
	assume ds:data, cs:code
	main proc 
		mov ax, data
		mov ds, ax

		lea si, num1							; write to offset of num1
		ask prompt1, si							; ask for first num
		lea di, val1							; store numeric value in offset of val1
		call string2num							; convert user input to numeric value
		
		lea si, num2							; do the same for second number
		ask prompt2, si
		lea di, val2
		call string2num

		mov ax, val1							; ADDITION
		add ax, val2
		lea si, answer
		call num2string

		show_result op1

		mov ax, val1							; SUBTRACTION
		sub ax, val2
		lea si, answer
		call num2string

		show_result op2

		mov ax, val1							; DIVISION
		div val2	
		lea si, answer
		call num2string	

		show_result op3

		mov ax, val1							; MULTIPLICATION
		mul val2	
		lea si, answer
		call num2string	

		show_result op4		

		mov ah, 4ch
		int 21h
	main endp

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
;------------------------------NUM2STRING BORROWED FROM PROGRAM 2------------------------------------
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
		mov cx, 7					; for the loop, since we have 7 characters to fill
		lea di, answer				; load the offset of numstring to destination index
		mov bl, '$'
		dollarloop:					; loop will terminate when count register == 0
			mov [di], bl
			inc di
			loop dollarloop
		
		ret
	dollarfiller endp
code ends
end main

