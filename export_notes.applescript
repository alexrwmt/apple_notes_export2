tell application "Notes"
    -- Создаем папку notes2, если она не существует
    do shell script "mkdir -p notes2"
    
    set allNotes to every note
    repeat with currentNote in allNotes
        -- Получаем название и содержимое заметки
        set noteTitle to name of currentNote
        set noteContent to body of currentNote
        
        -- Формируем безопасное имя файла (оставляем кириллицу и базовые символы)
        set safeTitle to do shell script "echo " & quoted form of noteTitle & " | iconv -f UTF-8 -t UTF-8//TRANSLIT | tr -cs '[:alnum:][:space:]А-Яа-я' '_' | tr -s '_' | tr '[:upper:]' '[:lower:]' | sed 's/^_//;s/_$//'"
        
        -- Создаем путь к файлу
        set filePath to "notes2/" & safeTitle & ".html"
        
        -- Записываем содержимое в файл
        do shell script "echo " & quoted form of noteContent & " > " & quoted form of filePath
    end repeat
end tell 