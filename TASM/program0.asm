.model small
.stack 100h
get macro text, offs						; macro to print prompt and get input
	lea dx, text
	mov ah, 09h
	int 21h
	
	mov dx, offs							; data segment offset where to store user input
	mov ah, 0ah								; 0ah is for getting an entire line of char
	int 21h

	lea dx, newline
	mov ah, 09h
	int 21h
endm
say macro text								; macro to print result
	lea dx, text
	mov ah, 09h
	int 21h
endm
data segment
	prompt1 db 'First value: $'
	prompt2 db 'Second value: $'
	yes db 'The values are equal.$'
	no db 'The values are not equal.$'
	firstval db 50 dup('$')					; stores the first user given value
	secondval db 50 dup('$')				; stores the second user given value
	newline db 10,13,'$'					; 10 = newline, 13 = carriage return
data ends
code segment
	assume ds:data, cs:code
	start:
		mov ax, data
		mov ds, ax

		lea si, firstval					; load offset address where to write 1st value 
		lea di, secondval					; load offset address where to write 2nd value 

		get prompt1, si						; get macro expansion
		get prompt2, di
		
		mov bx, 0000h
		
		mov bl, [si+1]						; these addresses store the digit count
		mov bh, [di+1]		

		cmp bl, bh							; if char count not equal, values are automatically different
		jne unequal

		compare:							; compare each digit
			mov bl, [si+1]
			mov bh, [di+1]
			cmp bl, bh
			jne unequal						; if not the same, say no
			inc si
			inc di
			cmp bl, '$'						; if terminating char reached, say yes
			jne compare						; else continue traversing number

		say yes								; say macro expansion
		jmp done

		unequal:
			say no							; no macro expansion

		done:
			mov ah, 4ch						; return control to DOS
			int 21h

code ends
end start