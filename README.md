# Приложение с графическим интерфейсом по получению ВЭКГ 

Векторная электрокардиография (ВЭКГ) - это метод, позволяющий измерять и представлять электрический вектор сердца во время сердечного цикла. Этот вектор представляет собой направление дипольного момента сердца, что дает информацию о сокращении сердечной мышцы. Врачи используют ВЭКГ для анализа движения вектора в трех основных плоскостях и его 3D отображения для диагностики и мониторинга состояния сердца. Такая информация может быть полезной для обнаружения аномалий, нарушений проводимости и оценки эффективности лечения. Векторная электрокардиография является важным инструментом в кардиологии и помогает улучшить диагностику и лечение сердечно-сосудистых заболеваний.

Данное приложение основано на его CLI версии - [get_VECG](https://github.com/Koldim2001/vector_ECG)

Код позвляет получать проекции и 3D представление ВЭКГ из исходных ЭКГ сигналов формата EDF, реализовывать систему поддержкии принятия решений (болен/здоров) на основе векторных петель, а так же определять информативные параметры данных петель.

Подробный pdf отчет о разработке доступен по ссылке - [__ОТЧЕТ__](https://github.com/Koldim2001/get_VECG_GUI/blob/main/Отчет%20о%20разработке.pdf) <br/>
### Видео туториалы: 
> 1. [__Презентация работы программы__](https://youtu.be/UTNPUhnxCF0)
> 2. [__Релиз приложения. Туториал по установке__](https://youtu.be/LBjjQQEMbTs)</br>
---
Загрузить exe файл (версия для врачей) можно по ссылке - [__ВЭКГ.exe__](https://drive.google.com/file/d/1NiJZQRy8RW_BnZ1ikotQ-E-WDKbNNe1F/view?usp=sharing)

---
## __УСТАНОВКА:__
Необходимо иметь установленный python 3 версии. \
Данные команды требуется запускать последовательно в терминале:
1. Склонируйте к себе этот репозиторий 
```
git clone https://github.com/Koldim2001/get_VECG_GUI.git
```
2. Перейдите с помощью команды cd в созданную папку get_VECG_GUI
```
cd get_VECG_GUI
```
3. Загрузите все необходимые библиотеки:
```
pip install -r requirements.txt
```
4. Запустите python скрипт:
```
python main.py
```

---
## __Окна программы:__
#### Главное окно приложения:
<div style="text-align:center;">
  <img src="https://drive.google.com/uc?id=1M1CS_xz3bp2w5g-34Dp01bDSXqz0sWIB" alt="normal" width="310" height="500">
</div>


#### Окна результатов обработки :
<div style="text-align:center;">
  <img src="https://drive.google.com/uc?id=1_0V8p5O-BlNBguF73Ja2bUhPGm3RNgRD" alt="pathology" width="900" height="470">
</div>


#### Окна промежуточных графических результатов обработки  :
<div style="text-align:center;">
  <img src="https://drive.google.com/uc?id=1zcntOImsxq99UwPvOOS4bfcm0d0OnEkY" alt="pathology" width="500" height="700">
</div>
 
---
### КАК СДЕЛАТЬ EXE:
```
pip install pyinstaller
pyinstaller --onefile -w --icon=configs/logo.ico main.py
```
<div style="text-align:center;">
  <img src="https://drive.google.com/uc?id=15zXrkRTfBcVQ-WGCkvp6QqQ-p_z98ETx" alt="pathology" width="150" height="150">
</div>
