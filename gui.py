# coding:utf-8
import sys
import gtk
from serial import Serial
from time import sleep

class ManipuladorGui:
    exec_list=[]
    
    def loadCommandsFile(self, commands_file="commands.txt"):
        arq=open(commands_file, 'r')
        lines=arq.readlines()
        for l in lines:
            self.exec_list.append(l[:-1])
    
    def realValue(self, graus, num_servo):
        """
        Função que retorna o valor a ser concatenado
        verifica pelo num_servo limitações quanto aos valores que podem ser passados a este
        """
        return graus
        
    def apiString(self):
        """
        Função que formata os dados já verificados e transformados por realValue
        ex:
        #5P500 #6P800 #4P1000 #3P1200 #2P1500 #1P2500
        #5P500 #6P800 #4P1000 #3P1200 #2P1500 #1P2500
        #5P700 #6P700 #4P700 #3P700 #2P700 #1P700
        """
        
        api_string=""
        i=0
        for s in self.servos:
            api_string=api_string+"#"+str(i+1)+"P"+str(self.realValue(s.get_value_as_int(), i))+" "#"T2000"+" "
            i=i+1
            
        return api_string[:-1]

    def reset_arm(self, objectToHandle):
        """
        Escrever na porta
        """
        
        #print self.apiString()
        
        arm_serial_file=self.entry1.get_text()
        arm_serial=Serial(arm_serial_file, 115200)
        arm_serial.write("#5P1500 #6P1500 #4P1500 #3P1500 #2P1500 #1P1500\n\r")
        
    def changed(self, objectToHandle):
        """
        Escrever na porta
        """
        
        #print self.apiString()
        
        arm_serial_file=self.entry1.get_text()
        arm_serial=Serial(arm_serial_file, 115200)
        arm_serial.write(self.apiString()+"\n\r")

    def addpos_rel(self, objectToHandle):
        """
        Obtém string de apiString e append em self.exec_list
        """
        print "pos salva"
        velocidade=self.velocity.get_value_as_int()
        print velocidade
        self.exec_list.append(self.apiString()+" T"+str(velocidade*1000))

    def rempos_rel(self, objectToHandle):
        """
        Obtém string de apiString e append em self.exec_list
        """
        print "pos removida"
        self.exec_list.pop()
                        
    def run_rel(self, objectTohandle):
        for p in self.exec_list:
            if p:
                print "posição executada", p
                arm_serial_file=self.entry1.get_text()
                arm_serial=Serial(arm_serial_file, 115200)
                arm_serial.write(p+"\n\r")
            sleep(2)
        
    def on_button1_released(self, objectToHandle):
        """
        Escrever na porta
        """
        
        #print self.apiString()
        
        arm_serial_file=self.entry1.get_text()
        arm_serial=Serial(arm_serial_file, 115200)
        arm_serial.write(self.apiString()+"\n\r")
            
    def __init__(self):
        
        builder = gtk.Builder()
        builder.add_from_file("gui.glade") 
        
        self.window1 = builder.get_object("window1")
        self.entry1 = builder.get_object("entry1")
        self.button1 = builder.get_object("button1")
        self.garra = builder.get_object("garra")
        self.pulso = builder.get_object("pulso")
        self.servo3 = builder.get_object("servo3")
        self.servo4 = builder.get_object("servo4")
        self.servo5 = builder.get_object("servo5")
        self.servo6 = builder.get_object("servo6")
        self.servo6 = builder.get_object("servo6")
        self.velocity = builder.get_object("velocity")
        
        adjustment = gtk.Adjustment(1, 0, 5, 1, 1, 0)
        self.velocity.set_adjustment(adjustment)
        
        builder.connect_signals(self)
        
        self.servos=[self.garra,
                     self.pulso,
                     self.servo3,
                     self.servo4,
                     self.servo5,
                     self.servo6]

        for s in self.servos:
            adjustment = gtk.Adjustment(1500, 500, 2500, 100, 100, 0)
            s.set_adjustment(adjustment)
        
        self.loadCommandsFile()
        
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()  
    
if __name__ == "__main__":
    gui = ManipuladorGui()
    gui.window1.show()
    gui.window1.show_all()
    gtk.main()
