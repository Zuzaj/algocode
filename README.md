# algoBLOCK

## Założenia programu
Nasz projekt to prosty język do nauki algorytmów, który ma na celu stworzenie łatwo zrozumiałego środowiska programistycznego. Dzięki prostej składni oraz intuicyjnym słowom kluczowym, użytkownicy będą mogli zrozumieć działanie algorytmów poprzez praktyczne wykorzystanie ich w kodzie.
1. Planowany wynik działania programu to interpreter języka pseudokodu, umożliwiający użytkownikom pisanie, testowanie i analizowanie działania algorytmów w czasie rzeczywistym.
2. Planowanym językiem implementacji jest Python. Do stworzenia interface graficznego użyjemy biblioteki GUI w Pythonie - Tkinter.
3. Planowana realizacja skanera oraz parsera poprzez użycie generatora parserów ANTLR 4.

## Opis języka
Nasz język programowania realizuje podstawowych elementów gramatyki języka programowania takie jak:
* definiowanie zmiennych liczbowych oraz tablic
* przypisywanie wartości do zmiennych i elementów tablic
* iterowanie przy użyciu pętli *for* oraz *while*
* określanie wartości wyrażenia boolowskiego
* warunkowe wykonanie bloku kodu dzięki słowow kluczowym *if* oraz *else*
* wykonywanie działań arytmetycznych na liczbach oraz zmiennych
* możliwość zwracania wartości przez program lub funkcję dzięki słowu kluczowemu *return*

Dodatkowo, biorąc pod uwagę docelowe zastosowanie naszego języka, zdecydowałyśmy się wprowadzić następujące ułatwienia: 
* wbudowana funkcja *print(arguments)* wyświetlająca na ekranie argumenty, lub w przypadku podania nazwy tablicy - wszystkie elementy tablicy
* wbudowana funckja *MIN_INDEX(array)* przyjmująca jako argument tablicę i zwracająca indeks najmniejszego elementu
* wbudowana funkcja *SWAP_VAR(argument1, argument2)* zamieniająca wartości argumentów
* wbudowana funkcja *SWAP_ARRAY(A\[index1], A\[index2])* zamieniająca wartości elementów tablicy o wskazanych indeksach
* wbudowana funkcja *length(array)* przyjmująca jako argument nazwę tablicy i zwracająca liczbę jej elementów
* możliwość definiowania i wywoływania własnych funkcji
* zdefiniowana dla użytkownika tablica **A = \[3, 7, 2, 4, 9, 5, 1]** dla usprawnienia testowania algorytmów sortujących

## Uruchomienie 
1. Pobierz repozytorium na swój komputer.
2. Zainstaluj pakiekt używając polecenia: `pip install antlr4-python3-runtime==4.13.1`
3. Uruchom plik `main.py`. Automatycznie otworzy się wtedy aplikacja okienkowa.

## Instrukcja obsługi
* Podstawowym działaniem aplikacji jest pisanie kodu w lewym oknie pola tekstowego. Następnie, gdy program jest już gotowy, należy kliknąć przycisk `RESULT`. Wtedy podany kod jest interpretowany i wynik działania jest przedstawiony w prawym oknie. 
* W górym menu aplikacji jest możliwość skorzystania z opcji `Słowa kluczowe`. Po wybraniu intrukcji, którą chcemy użyć w naszym kodzie jest ona zapisywana do schowka, przez co łatwo można ją stosować w kodzie (`Ctrl+V`).
* Wynik analizy składniowej można zobaczyć w pliku `formatted_tree.txt`.

## Tokeny
- TOK_FUNC : 'function';
- TOK_ASSIGN: '=';
- TOK_IS_EQUAL: '?=';
- TOK_NOT_EQUAL: '/=';
- TOK_SMALLER: '<';
- TOK_SMALLER_EQ: '<=';
- TOK_GREATER: '>';
- TOK_GREATER_EQ: '>=';
- TOK_PLUS: '+';
- TOK_MINUS: '-';
- TOK_EL: '*';
- TOK_DIV: '/';
- TOK_TAB_L: '[';
- TOK_TAB_R: ']';
- TOK_ARG_L: '(';
- TOK_ARG_R: ')';
- TOK_WS: (' ' | '\t' | '\n') -> skip;
- TOK_FOR : 'for';
- TOK_WHILE : 'while';
- TOK_IF : 'if';
- TOK_ELSE: 'else';
- TOK_DO : 'do';
- TOK_TO : 'to';
- TOK_THEN : 'then';
- TOK_LEN : 'length';
- TOK_RETURN : 'return';
- TOK_AND : 'and';
- TOK_OR : 'or';
- TOK_END_FUNC : 'endfunction';
- TOK_DOWNTO : 'downto';
- TOK_COM : ',';
- TOK_ARROW_L : '->';
- TOK_ARROW_R : '>-';
- TOK_VAR: [a-zA-Z_]+;
- TOK_NUM: [0-9]+([.][0-9]+)?;

## Gramatyka
```g4
program: code EOF ;

code: (function_def | statement)+;

function_def: TOK_FUNC TOK_VAR TOK_ARG_L arguments? TOK_ARG_R (statement)* return_statement? TOK_END_FUNC;

function_call:   TOK_VAR TOK_ARG_L arguments? TOK_ARG_R;

argument: expression;

arguments: argument (TOK_COM argument)*;

statement:  (TOK_EL (assignment | array_def | function_call)) | ( for_loop | if_statement | if_else_statement | if_return_statement | while_statement );

assignment:  (TOK_VAR | array_call) TOK_ASSIGN expression;

bool_expression: ( TOK_VAR | TOK_NUM | array_call )
                (TOK_IS_EQUAL | TOK_NOT_EQUAL | TOK_SMALLER | TOK_GREATER | TOK_GREATER_EQ | TOK_SMALLER_EQ)
                 ( TOK_VAR | TOK_NUM | array_call) 
                 ((TOK_AND | TOK_OR)  
                 ( TOK_VAR | TOK_NUM | array_call ) 
                 (TOK_IS_EQUAL | TOK_NOT_EQUAL | TOK_SMALLER | TOK_GREATER | TOK_SMALLER_EQ | TOK_GREATER_EQ)
                ( TOK_VAR | TOK_NUM | array_call))*;

for_loop: TOK_FOR TOK_VAR TOK_ASSIGN expression (TOK_TO | TOK_DOWNTO) expression TOK_DO TOK_ARROW_L (statement)+ TOK_ARROW_R;

if_else_statement: if_statement (else_statement | else_return_statement);

else_statement: TOK_ELSE TOK_ARROW_L (statement)+ TOK_ARROW_R;

else_return_statement: TOK_ELSE TOK_ARROW_L (statement)* return_statement TOK_ARROW_R;

if_return_statement: TOK_IF bool_expression TOK_THEN TOK_ARROW_L (statement)* return_statement TOK_ARROW_R;

if_statement:  TOK_IF bool_expression TOK_THEN TOK_ARROW_L (statement)+  TOK_ARROW_R;

while_statement: TOK_WHILE bool_expression TOK_DO TOK_ARROW_L (statement)+ TOK_ARROW_R;

array_def:   TOK_VAR TOK_ASSIGN TOK_TAB_L TOK_TAB_R;

array_call: TOK_VAR TOK_TAB_L 
            ( expression | function_call)
            TOK_TAB_R;

return_statement: TOK_RETURN (TOK_VAR | TOK_NUM);


expression: TOK_VAR
           | TOK_NUM
           | array_call
           | expression TOK_PLUS expression
           | expression TOK_MINUS expression
           | expression TOK_DIV expression
           | TOK_LEN TOK_ARG_L TOK_VAR TOK_ARG_R
           | function_call;
```

## Pakiety zewnętrzne
Wykorzystanie ANTLR4 (ANother Tool for Language Recognition) do generowania skanerów i parserów umożliwia szybkie i efektywne tworzenie analizatorów składniowych dla różnorodnych języków programowania oraz specyfikacji formalnych.



## Przykłady użycia 
Przykładowy kod obrazujący budowę języka:
```
function INSERTION_SORT()
    for j = 2 to length(A)-1 do ->
       * key = A[j]
       * i = j - 1
        while i > 0 and A[i] > key do ->
          * A[i + 1] = A[i]
          * i = i - 1
         >-
       * A[i+1] = key
       *print(A)
    >-
endfunction

* INSERTION_SORT()
* print(A)
```
Inne proponowane przykłady algorytmów do przetestowania działania języka znajdują się w folderze [algorithms](./algorithms/).





