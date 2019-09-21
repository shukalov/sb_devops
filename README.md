# Требования

 1. Написать ansible-playbook с помощью которого можно установить jenkins + docker.
 2. Написать pipeline который соберет docker образ с простеньким скриптом на python, и запустит контейнер из этого образа.
 3. Результат включающий в себя ansible-playbook dockerfile pipeline-script, просьба опубликовать в git репозитории (Gitlab Github Bitbucket и т.д.) и прислать ссылку на него.

Будет плюсом если в репозитории будет содержаться вся история работы над проектом.


# Мои комментарии

 1. В связи с тем, что OS указана не была, взял Debian-based, для
    проверки конкретно Ubuntu 18.04. Структура проекта взята из [Best
    Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
    (второй вариант). Декларативное описание состояния stage площадки (с комментариями)
    находится в **ansible/inventories/stage/group_vars/sberbank.yml**

    **Разворачивание:**
    **ansible-playbook -i ansible/inventories/stage/ ansible/all.yml**

 2. В качество простенького python скрипта в docker контейнере взял задание с предыдущего собеседования. Вся структура в каталоге **docker**.
 3. Pipeline соответственно в **pipeline/sb_docker.jenkinsfile**. Docker контейнер соответственно собирается из этого же репозитория.

Если что-то нужно доработать - доработаю. Буду благодарен за любую обратную связь, особенно за отрицательную.
