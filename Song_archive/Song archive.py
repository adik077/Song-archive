from tkinter import*
from tkinter import messagebox
import pickle
import fpdf
import os
import webbrowser

class Initialize:
    def __init__(self,name, artist,url):
        self.name=name
        self.artist=artist
        self.url=url

class PDF_creator:
    def __init__(self,song_list):
        self.song_list=song_list
        
    def create_pdf(self):
        self.helper=''
        self.pdf=fpdf.FPDF(format='A4')
        self.pdf.add_page()
        self.pdf.set_font('Arial',size=12)
        self.pdf.cell(60,10,'SONG')
        self.pdf.cell(35,10,'AUTHOR')
        self.pdf.cell(40,10,'URL')
        self.pdf.set_line_width(0.5)
        self.pdf.set_draw_color(255,0,0)
        self.pdf.line(10,20, 200,20)
        self.pdf.ln()
        
        ######### SORTING ###########
        for i in range(0,len(self.song_list)-1):
            for a in range(0,len(self.song_list)-1-i):
                if (self.song_list[a].name>self.song_list[a+1].name):
                    self.helper=self.song_list[a]
                    self.song_list[a]=self.song_list[a+1]
                    self.song_list[a+1]=self.helper
        ######### SORTING ###########
        
        for song in self.song_list:
            self.pdf.cell(60,10,song.name)
            self.pdf.cell(35,10,song.artist)
            self.pdf.cell(40,10,song.url)
            self.pdf.ln()
        self.pdf.output('Song archive.pdf')
        os.startfile('Song archive.pdf')
        

class Front_End:
    def start(self, song_list):
        self.found_songs=[]
        self.song_list=song_list
        self.iterator=0
        self.name_helper=''
        self.artist_helper=''
        self.url_helper=''
        
        def add_song():
            name=self.name_entry.get()
            artist=self.artist_entry.get()
            url=self.url_entry.get()
            self.check=False
            self.check2=False
            
            if name=='':
                self.name_entry.config(bg='red')
                self.check=True
            if artist=='':
                self.artist_entry.config(bg='red')
                self.check=True
            if url=='':
                self.url_entry.config(bg='red')
                self.check=True
                
            for i in self.song_list:
                if ((i.name==name) and (i.artist==artist) and (i.url==url)):
                    self.check=True
                    self.check2=True
                    
            if self.check==False:
                song=Initialize(name, artist, url)
                self.song_list.append(song)
                clear()
                self.record_exist_label.config(text='SONG ADDED', fg='blue')
                
            else:
                pass
            if self.check2==True:
                self.record_exist_label.config(text='RECORD ALREADY EXISTS', fg='red')
            else:
                pass



        def clear():
            self.name_entry.delete(0,END)
            self.artist_entry.delete(0,END)
            self.url_entry.delete(0,END)
            self.name_entry.config(bg='white')
            self.artist_entry.config(bg='white')
            self.url_entry.config(bg='white')
            self.song_counter_label.config(text='')
            self.record_exist_label.config(text='')

        def save():
            for song in self.song_list:
                if ((song.name==self.name_helper)and (song.artist==self.artist_helper)and(song.url==self.url_helper)):
                    song.name=self.name_entry.get()
                    song.artist=self.artist_entry.get()
                    song.url=self.url_entry.get()
                    break
            with open('song list.sl','wb') as file:
                pickle.dump(self.song_list,file)
            


        def search():
            clear()
            self.iterator=0
            self.found_songs=[]
            for searched_song in self.song_list:
                    if ((searched_song.name.upper()==self.search_entry.get().upper()) or (searched_song.artist.upper()==self.search_entry.get().upper())):
                        self.name_entry.delete(0,END)
                        self.artist_entry.delete(0,END)
                        self.url_entry.delete(0,END)

                        self.found_songs.append(searched_song)
                        
            if self.found_songs:
                self.name_entry.insert(0,self.found_songs[0].name)
                self.artist_entry.insert(0,self.found_songs[0].artist)
                self.url_entry.insert(0,self.found_songs[0].url)
                self.song_counter_label.config(text=('Song',self.iterator+1,'/',len(self.found_songs)), fg='gray')

                #saving actually shown values to allow edit them
                self.name_helper=self.found_songs[0].name
                self.artist_helper=self.found_songs[0].artist
                self.url_helper=self.found_songs[0].url
                
            else:
                clear()
                self.name_entry.insert(0,'Field not found')
                self.artist_entry.insert(0,'Field not found')
                self.url_entry.insert(0,'Field not found')       
        def right():
            clear()
            self.iterator=self.iterator+1
            if (self.iterator>(len(self.found_songs)-1)):
                self.iterator=(len(self.found_songs)-1)
            self.name_entry.insert(0,self.found_songs[self.iterator].name)
            self.artist_entry.insert(0,self.found_songs[self.iterator].artist)
            self.url_entry.insert(0,self.found_songs[self.iterator].url)
            self.song_counter_label.config(text=('Song',self.iterator+1,'/',len(self.found_songs)), fg='gray')

            #saving actually shown values to allow edit them
            self.name_helper=self.found_songs[self.iterator].name
            self.artist_helper=self.found_songs[self.iterator].artist
            self.url_helper=self.found_songs[self.iterator].url
            
        def left():
            clear()
            self.iterator=self.iterator-1
            if self.iterator<0:
               self.iterator=0
            self.name_entry.insert(0,self.found_songs[self.iterator].name)
            self.artist_entry.insert(0,self.found_songs[self.iterator].artist)
            self.url_entry.insert(0,self.found_songs[self.iterator].url)
            self.song_counter_label.config(text=('Song',self.iterator+1,'/',len(self.found_songs)), fg='gray')

            #saving actually shown values to allow edit them
            self.name_helper=self.found_songs[self.iterator].name
            self.artist_helper=self.found_songs[self.iterator].artist
            self.url_helper=self.found_songs[self.iterator].url

        def create_pdf():
            pdf_create=PDF_creator(self.song_list)
            pdf_create.create_pdf()

        def delete_record():
            if ((self.name_entry.get()=='') and (self.artist_entry.get()=='') and (self.url_entry.get()=='')):
                 pass
            else:
                status=messagebox.askokcancel(title='Confirm', message='Are You sure You want to delete actual record?')
                if status==True:
                    name_to_del=self.name_entry.get()
                    artist_to_del=self.artist_entry.get()
                    url_to_del=self.url_entry.get()
                    for song in self.song_list:
                        if ((song.name==name_to_del) and (song.artist==artist_to_del) and (song.url==url_to_del)):
                            self.song_list.remove(song)
                            break
                    clear()
                    self.record_exist_label.config(text='RECORD REMOVED', fg='blue')
                else:
                    pass

        def open_link():
            opener=self.url_entry.get()
            webbrowser.open(opener)
            
                

        
        root=Tk()
        root.resizable(width=False, height=False)
        root.title('Song archive')
        root.geometry("400x400")
        iterator=0


        name_label=Label(root, text='Song')
        name_label.grid(row=0, column=0, padx=5, pady=5, stick=W)

        self.name_entry=Entry(root, width=30, bg='white')
        self.name_entry.grid(row=1, column=0, padx=5, pady=5, stick=E+W)

        artist_label=Label(root, text='Artist')
        artist_label.grid(row=2, column=0, padx=5, pady=5, stick=W)

        self.artist_entry=Entry(root,width=30, bg='white')
        self.artist_entry.grid(row=3, column=0, padx=5, pady=5, stick=E+W)

        url_label=Label(root, text='URL')
        url_label.grid(row=4, column=0, padx=5, pady=5, stick=W)


        self.url_entry=Entry(root,width=30, bg='white')
        self.url_entry.grid(row=5, column=0, padx=5, pady=5, stick=E+W)

        add_song_button=Button(root,text='Add Song', command=add_song, width=8)
        add_song_button.grid(row=6, column=0, padx=5, pady=5, stick=E)

        clear_button=Button(root,text='Clear', command=clear, width=8)
        clear_button.grid(row=6, column=0, padx=5, pady=5,rowspan=2, stick=W)

        search_label=Label(root, text='Find song')
        search_label.grid(row=0, column=1, padx=5, pady=5, stick=W)

        self.search_entry=Entry(root, width=32)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)
        self.search_entry.insert(0,'Song name/Artist')
        self.search_entry.config(fg='gray')
        
        search_button=Button(root,text='Search', command=search, width=8).place(x=330,y=65)

        save_button=Button(root,text='Save', command=save, width=8).place(x=330, y=370)
        
        next_button=Button(root,text='>>', command=right).place(x=160, y=5)
        prev_button=Button(root,text='<<', command=left).place(x=130, y=5)

        self.song_counter_label=Label(root, text='')
        self.song_counter_label.grid(row=0, column=0)

        self.record_exist_label=Label(root, text='', fg='red')
        self.record_exist_label.grid(row=8, column=0)

        pdf_button=Button(root,text='PDF', command=create_pdf, width=8).place(x=330,y=185)
        delete_button=Button(root,text='DEL', command=delete_record, width=8).place(x=330,y=100)
        open_link_button=Button(root,text='...', command=open_link, width=2, height=1).place(x=190,y=152)

        
        root.mainloop()
       

try:
    with open('song list.sl','rb') as file:
        song_list=[]
        song_list=pickle.load(file)
except:
        song_list=[]

start=Front_End()
start.start(song_list)
