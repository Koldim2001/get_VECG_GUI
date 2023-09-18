import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import hydra
from functions import *



@hydra.main(version_base=None, config_path="configs", config_name="app_config")
def main(config: dict) -> None:

    def enter_data():
        # Главный обработчик кнопки запуск
        if file_path is not None:
            input_data = {}
            input_data["data_edf"] = file_path
            if '.edf' not in file_path:
                tkinter.messagebox.showerror("Ошибка", "Файл EDF не выбран")
                return
            
            try:
                input_data["n_term_start"] = int(n_term_start.get())
            except ValueError:
                tkinter.messagebox.showerror("Ошибка", "Невозможно преобразовать номер периода ЭКГ в целое число")
                return
            
            input_data["n_term_finish"] = None
            input_data["filt"] = filt.get()

            if not input_data["filt"]:
                input_data["f_sreza"] = None
            else:
                try:
                    input_data["f_sreza"] = float(f_sreza.get())
                except ValueError:
                    tkinter.messagebox.showerror("Ошибка", "Невозможно преобразовать частоту среза в число с плавающей точкой")
                    return
            
            try:
                input_data["f_sampling"] = float(f_sampling.get())
            except ValueError:
                tkinter.messagebox.showerror("Ошибка", "Невозможно преобразовать частоту дискретизации в число с плавающей точкой")
                return
            
            input_data["show_ecg"] = show_ECG.get()
            input_data["plot_3d"] = plot_3D.get()
            input_data["qrs_loop_area"] = QRS_loop_area.get()
            input_data["t_loop_area"] = T_loop_area.get()
            input_data["count_qrst_angle"] = count_qrst_angle.get()
            input_data["mean_filter"] = mean_filter.get()
            input_data["predict"] = predict_res.get()
            input_data["plot_projections"] = plot_projections.get()
            res = get_VECG(input_data)

            message = []
            if res == 'no_this_period':
                tkinter.messagebox.showerror("Ошибка", "Не найден такой период. Попробуйте ввести меньше значение")
            if res == 'too_noisy':
                tkinter.messagebox.showerror("Ошибка", "Не получилось построить ВЭКГ, так как ЭКГ слишком шумный")
            if len(res) == 4:
                area_projections, angle_qrst, angle_qrst_front, message_predict = res
                if input_data["predict"]:
                    message.append('СППР: ' + message_predict)
                if input_data["qrs_loop_area"]:
                    message.append(f'Площадь петли QRS во фронтальной плоскости: {"{:.3e}".format(area_projections[0])}')
                    message.append(f'Площадь петли QRS во сагиттальной плоскости: {"{:.3e}".format(area_projections[1])}')
                    message.append(f'Площадь петли QRS во аксиальной плоскости: {"{:.3e}".format(area_projections[2])}')
                if len(area_projections) == 6:
                    message.append(f'Площадь петли ST-T во фронтальной плоскости: {"{:.3e}".format(area_projections[3])}')
                    message.append(f'Площадь петли ST-T во сагиттальной плоскости: {"{:.3e}".format(area_projections[4])}')
                    message.append(f'Площадь петли ST-T во аксиальной плоскости: {"{:.3e}".format(area_projections[5])}')
                elif input_data["t_loop_area"]:
                    message.append(f'Площадь петли ST-T во фронтальной плоскости: {"{:.3e}".format(area_projections[0])}')
                    message.append(f'Площадь петли ST-T во сагиттальной плоскости: {"{:.3e}".format(area_projections[1])}')
                    message.append(f'Площадь петли ST-T во аксиальной плоскости: {"{:.3e}".format(area_projections[2])}')
                if input_data["count_qrst_angle"]:
                    message.append(f'Пространственный угол QRST равен {round(angle_qrst, 2)} градусов')
                    #message.append(f'Проекция угла QRST на фронтальную плоскость равна {round(angle_qrst_front, 2)} градусов')


                for widget in res_frame.winfo_children():
                    widget.destroy()

                # Вывод результатов:
                for i, text in enumerate(message):
                    if 'Здоров' in text:
                        label = tkinter.Label(res_frame, text=text, foreground='#126E18', font=('bold', 10))
                    elif 'Болен' in text:
                        label = tkinter.Label(res_frame, text=text, foreground='#8B0000', font=('bold', 10))
                    else:
                        label = tkinter.Label(res_frame, text=text)
                    label.grid(row=i, column=0, sticky="w")

        else:
            tkinter.messagebox.showwarning("Ошибка", "Не выбран файл")


    def close_all_plots():
        # Закрытие всех графиков 
        plt.close('all')


    def toggle_f_sreza_entry():
        # Позволяет убрать поле f_sreza если выключен фильтр
        if filt.get():
            f_sreza_label.grid(row=3, column=0, padx=10, pady=2)
            f_sreza.grid(row=3, column=1, padx=10, pady=2)
        else:
            f_sreza_label.grid_forget()
            f_sreza.grid_forget()
        

    def open_file():
        # Позволяет пользователю выбрать файл и его отображает в label
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("EDF files", "*.edf")])  
        if file_path:
            file_name = os.path.basename(file_path)  # Получаем имя файла из полного пути
            file_label.config(text=f"Выбран файл: {file_name}")
        else:
            file_label.config(text="Файл не выбран")
        return file_path

    window = tkinter.Tk()
    window.title("Получение ВЭКГ")
    icon = tkinter.PhotoImage(file=config['logo'])
    window.iconphoto(True, icon)
    
    # Создание главного окна приложения
    frame = tkinter.Frame(window)
    frame.pack()

    #############

    # Основное поле
    info_frame =tkinter.LabelFrame(frame, text="")
    info_frame.grid(row= 0, column=0, padx=10, pady=5)

    n_term_text = tkinter.Label(info_frame, text="Номер периода ЭКГ")
    n_term_start = tkinter.Spinbox(info_frame, from_=config['n_term_begin'],
                                  to=config['n_term_end'])
    n_term_start.delete(0, "end")  # Очищаем начальное значение
    n_term_start.insert(0, config['n_term_start'])  # Устанавливаем начальное значение
    n_term_text.grid(row=0, column=0, padx=45, pady=5)
    n_term_start.grid(row=1, column=0, padx=45, pady=5)

    open_button = tkinter.Button(info_frame, text="Открыть файл", command=open_file)
    open_button.grid(row=1, column=1, padx=45, pady=5)

    file_label = tkinter.Label(info_frame, text="Файл не выбран")
    file_label.grid(row=0, column=1, padx=5, pady=5)
    

    ##############

    # Поле выбора режимов
    type_frame = tkinter.LabelFrame(frame, text="Выбор режимов")
    type_frame.grid(row=1, column=0, sticky="news", padx=20, pady=5)

    plot_projections = tkinter.BooleanVar(value=config['plot_projections'])
    plot_projections_check = tkinter.Checkbutton(type_frame, text= "Построение проекций ВЭКГ",
                                    variable=plot_projections, onvalue=True, offvalue=False)
    plot_projections_check.pack(anchor="w", pady=2, padx=100)


    plot_3D = tkinter.BooleanVar(value=config['plot_3D'])
    plot_3D_check = tkinter.Checkbutton(type_frame, text= "Построение 3D ВЭКГ",
                                    variable=plot_3D, onvalue=True, offvalue=False)
    plot_3D_check.pack(anchor="w", pady=2, padx=100)


    show_ECG = tkinter.BooleanVar(value=config['show_ECG'])
    show_ECG_check = tkinter.Checkbutton(type_frame, text= "Отображение ЭКГ сигналов",
                                    variable=show_ECG, onvalue=True, offvalue=False)
    show_ECG_check.pack(anchor="w", pady=2, padx=100)


    predict_res = tkinter.BooleanVar(value=config['predict_res'])
    predict_res_check = tkinter.Checkbutton(type_frame, text= "Результат СППР (болен/здоров)",
                                    variable=predict_res, onvalue=True, offvalue=False)
    predict_res_check.pack(anchor="w", pady=2, padx=100)


    count_qrst_angle = tkinter.BooleanVar(value=config['count_qrst_angle'])
    count_qrst_angle_check = tkinter.Checkbutton(type_frame, text= "Расчет угла QRST",
                                    variable=count_qrst_angle, onvalue=True, offvalue=False,)
    count_qrst_angle_check.pack(anchor="w", pady=2, padx=100)


    QRS_loop_area = tkinter.BooleanVar(value=config['QRS_loop_area'])
    QRS_loop_area_check = tkinter.Checkbutton(type_frame, text= "Расчет площади QRS петли",
                                    variable=QRS_loop_area, onvalue=True, offvalue=False,)
    QRS_loop_area_check.pack(anchor="w", pady=2, padx=100)


    T_loop_area = tkinter.BooleanVar(value=config['T_loop_area'])
    T_loop_area_check = tkinter.Checkbutton(type_frame, text= "Расчет площади ST-T петли",
                                    variable=T_loop_area, onvalue=True, offvalue=False,)
    T_loop_area_check.pack(anchor="w", pady=2, padx=100)

    close_button = tkinter.Button(type_frame, text="Закрыть все имеющиеся графики", command=close_all_plots)
    close_button.pack(anchor="center", pady=5, padx=50)


    #####################

    # Поле настроек
    settings_frame = tkinter.LabelFrame(frame, text="Настройки")
    settings_frame.grid(row=2, column=0, sticky="news", padx=20, pady=5)

    mean_filter = tkinter.BooleanVar(value=config['mean_filter'])
    mean_filter_check = tkinter.Checkbutton(settings_frame, text= "Сглаживание петель",
                                    variable=mean_filter, onvalue=True, offvalue=False)
    mean_filter_check.grid(row=0, column=0, columnspan=2)


    filt = tkinter.BooleanVar(value=config['filt'])
    filt_value_check = tkinter.Checkbutton(settings_frame, text= "ФВЧ фильтрация ЭКГ сигналов",
                                    variable=filt, onvalue=True, offvalue=False, command=toggle_f_sreza_entry)
    filt_value_check.grid(row=1, column=0, columnspan=2)
 

    Fs_label = tkinter.Label(settings_frame, text="Частота дискретизации (в Гц)")
    Fs_label.grid(row=2, column=0, padx=22, pady=2)
    f_sampling = tkinter.Entry(settings_frame)
    f_sampling.grid(row=2, column=1, padx=22, pady=2)
    f_sampling.insert(0, config['f_sampling'])  # Установление значения по умолчанию 


    f_sreza_label = tkinter.Label(settings_frame, text="Частота среза ФВЧ фильтра (в Гц)")    
    f_sreza = tkinter.Entry(settings_frame)
    f_sreza.insert(0, config['f_sreza'])  # Установление значения по умолчанию
    toggle_f_sreza_entry()
    

    ##################

    # Кнопка запуска
    custom_font = ("Helvetica", 10, "bold")
    button = tkinter.Button(frame, text="Запуск", bg="#0074D9", fg="white",
                            font=custom_font,  command=enter_data)
    button.grid(row=3, column=0, sticky="news", padx=30, pady=10)
   
    # Инициализация поля результатов
    res_frame = tkinter.LabelFrame(frame, text="Результаты")
    res_frame.grid(row=4, column=0, sticky="news", padx=30, pady=5)
 
    window.mainloop()


if __name__ == "__main__":
    file_path = None
    main()
