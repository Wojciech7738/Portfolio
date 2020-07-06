using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml.Linq;
using System.Drawing.Printing;

namespace photoviewer
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            var args = Environment.GetCommandLineArgs();
            if (args.Length != 1)
            {
                pictureBox1.Load(args[1]);
                openFlag = true;
            }

            if (File.Exists("colors.xml"))
            {
                XDocument xml1 = XDocument.Load("colors.xml");
                
                int a = Convert.ToInt32(xml1.Root.Element("A").Value);
                int r = Convert.ToInt32(xml1.Root.Element("R").Value);
                int g = Convert.ToInt32(xml1.Root.Element("G").Value);
                int b = Convert.ToInt32(xml1.Root.Element("B").Value);
                Color c = Color.FromArgb(a, r, g, b);
                set_colors(c);
            }
                
        }
        
        public bool openFlag = false;//Do drukowania

        private void save_to_file(int A, int R, int G, int B)
        {
            List<int> colors = new List<int>();
            colors.Add(A);
            colors.Add(R);
            colors.Add(G);
            colors.Add(B);

            XDocument xml = new XDocument(
                new XDeclaration("1.0", "utf-8", "yes"),
                new XComment("Lista kolorów"),
                new XElement("Kolory",
                        new XElement("A", colors[0]),
                        new XElement("R", colors[1]),
                        new XElement("G", colors[2]),
                        new XElement("B", colors[3])
                )
            );
            xml.Save("colors.xml");
        }


        private void set_colors(Color color)
        {
                pictureBox1.BackColor = color;

                close_button2.BackColor = color;
                setButton.BackColor = color;
                clearButton.BackColor = color;
                printButton.BackColor = color;
                button1.BackColor = color;

                if (color.A + color.R + color.G + color.B < 480)
                {
                    close_button2.ForeColor = System.Drawing.Color.White;
                    setButton.ForeColor = System.Drawing.Color.White;
                    clearButton.ForeColor = System.Drawing.Color.White;
                    printButton.ForeColor = System.Drawing.Color.White;
                    button1.ForeColor = System.Drawing.Color.White;
                }
                else
                {
                    close_button2.ForeColor = System.Drawing.Color.Black;
                    setButton.ForeColor = System.Drawing.Color.Black;
                    clearButton.ForeColor = System.Drawing.Color.Black;
                    printButton.ForeColor = System.Drawing.Color.Black;
                    button1.ForeColor = System.Drawing.Color.Black;
                }
                this.BackColor = color;
        }


        private void Button1_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                pictureBox1.Load(openFileDialog1.FileName);
                openFlag = true;
                //pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            }
        }

        private void SetButton_Click(object sender, EventArgs e)
        {
            if (colorDialog1.ShowDialog() == DialogResult.OK)
            {
                set_colors(colorDialog1.Color);
                save_to_file(colorDialog1.Color.A, colorDialog1.Color.R, colorDialog1.Color.G, colorDialog1.Color.B);
            }
        }

        private void ClearButton_Click(object sender, EventArgs e)
        {
            pictureBox1.Image = null;
        }

        private void close_button2_Click(object sender, EventArgs e)
        {
            this.Close();
        }


        //Drukowanie

        private void printDocument1_PrintPage(object sender, PrintPageEventArgs e)
        {
            System.Drawing.Image img = System.Drawing.Image.FromFile(openFileDialog1.FileName);
            Point loc = new Point(0, 0);
            e.Graphics.DrawImage(img, loc);
        }


        private void PrintButton_Click(object sender, EventArgs e)
        {
            if (openFlag == true)
            {
                PrintDocument pd = new PrintDocument();
                pd.PrintPage += printDocument1_PrintPage;
                PrintPreviewDialog printPreviewDialog1 = new PrintPreviewDialog();
                printPreviewDialog1.Document = pd;
                printPreviewDialog1.ShowDialog();
                //pd.Print();
            }
        }

    }
}
