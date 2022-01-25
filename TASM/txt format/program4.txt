.model small
.stack 100h
get macro text, offs						; macro to print prompt and get input
	lea dx, text
	mov ah, 09h
	int 21h
	
	mov dx, offs							; offs = where to start writing the user input
	mov ah, 0ah
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
	prompt1 db 'First string: $'
	prompt2 db 'Second string: $'
	yes db 'The strings are the same.$'
	no db 'The strings are not the same.$'
	firststr db 50 dup('$')					; stores the first user given string
	secondstr db 50 dup('$')				; stores the second user given string
	newline db 10,13,'$'					; 10 = newline, 13 = carriage return
data ends
code segment
	assume ds:data, cs:code
	start:
		mov ax, data
		mov ds, ax

		lea si, firststr					; load offset address where to write 1st string 
		lea di, secondstr					; load offset address where to write 2nd string 

		get prompt1, si						; get macro expansion
		get prompt2, di
		
		mov bx, 0000h
		
		mov bl, [si+1]						; these addresses store the character count
		mov bh, [di+1]		

		cmp bl, bh							; if char count not equal, strings are automatically different
		jne unequal

		compare:							; compare each character
			mov bl, [si+1]
			mov bh, [di+1]
			cmp bl, bh
			jne unequal						; if not the same, say no
			inc si
			inc di
			cmp bl, '$'						; if terminating char reached, say yes
			jne compare						; else continue traversing strings

		say yes								; say macro expansion
		jmp done

		unequal:
			say no							; no macro expansion

		done:
			mov ah, 4ch						; return control to DOS
			int 21h

code ends
end start