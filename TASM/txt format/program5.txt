.model small
.stack 100h
nextline macro								; merely prints a newline
	lea dx, newline
	mov ah, 09h
	int 21h
endm
data segment
	prompt db 'Enter a string: $'
	firstch db 'First character: $'
	lastch db 'Last character: $'
	the_string db 20 						; max chars able to hold including newline char when user presses Enter
			   db ?							; how many characters actually entered by user
			   db 20 dup('$')				; where the string itself is stored
	newline db 10,13,'$'
data ends
code segment
	assume ds:data, cs:code
	start:
		mov ax, data
		mov ds, ax

		lea si, the_string					; load offset of the_string to source index

		lea dx, prompt						; say 'Enter a string: '
		mov ah, 09h
		int 21h

		mov dx, si							; get user string, write at location in si			
		mov ah, 0ah							; 0ah is a getline function
		int 21h

		nextline

		lea dx, firstch						; say 'First character: '
		mov ah, 09h
		int 21h

		mov dx, [si+2]						; 1st byte = size of arr, 2nd byte = actual size
		mov ah, 02h
		int 21h

		nextline

		lea dx, lastch						; say 'Last character: '
		mov ah, 09h
		int 21h

		lea si, the_string+2				; start search from first char
	
		l1:									; loop to find last char
			mov dx, [si]
			inc si	
			cmp dl, '$'						; terminating character found
			jne l1							; stop searching
	
			mov dx, [si-3]					; 3 because there are 2 dollar signs and 1 newline character before last char 
			mov ah, 02h
			int 21h		

		mov ah, 4ch
		int 21h
		
code ends
end start