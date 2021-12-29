#include <vtkAutoInit.h>
VTK_MODULE_INIT(vtkRenderingOpenGL2); // VTK was built with vtkRenderingOpenGL2
VTK_MODULE_INIT(vtkInteractionStyle);


#include <vtkActor.h>
#include <vtkCamera.h>
#include <vtkSTLWriter.h>
#include <vtkMarchingCubes.h>
#include <vtkMetaImageReader.h>
#include <vtkNamedColors.h>
#include <vtkOutlineFilter.h>
#include <vtkPolyDataMapper.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSmartPointer.h>
#include <vtkStripper.h>
#include <stdio.h>
#include <io.h>
#include<string>
#include <array>
#include <vtkSmartPointer.h>
#include <vtkActor.h>
#include <vtkDelaunay2D.h>
#include <vtkMath.h>
#include <vtkPoints.h>
#include <vtkSTLWriter.h>
#include <vtkSTLReader.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmoothPolyDataFilter.h>
#include <vtkPolyDataNormals.h>
#include <vtkCamera.h>
#include <vtkActor.h>
#include<Windows.h>
#include<time.h>
#include <vtkImageWriter.h>
#include <vtkJPEGWriter.h>
#include <vtkCamera.h>
#include <vtkClipPolyData.h>
#include <vtkDataSetMapper.h>
#include <vtkFeatureEdges.h>
#include <vtkNamedColors.h>
#include <vtkPlane.h>
#include <vtkWindowToImageFilter.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkStripper.h>
#include <vtkXMLPolyDataReader.h>
#include<sstream>

// Readers
#include <vtkBYUReader.h>
#include <vtkOBJReader.h>
#include <vtkPLYReader.h>
#include <vtkPolyDataReader.h>
#include <vtkSTLReader.h>
#include <vtkOutlineFilter.h>
#include <vtkXMLPolyDataReader.h>
#include <vtkSmoothPolyDataFilter.h>
#include <vtkPolyDataNormals.h>
#include <vtkSphereSource.h>
#include<fstream>
#include<iostream>




namespace {
    vtkSmartPointer<vtkPolyData> ReadPolyData(std::string const& fileName);
    void WriteImage(std::string const& fileName, vtkRenderWindow* renWin, bool rgba)
    {
        std::string fn = fileName;

        auto writer = vtkSmartPointer<vtkImageWriter>::New();

        writer = vtkSmartPointer<vtkJPEGWriter>::New();

        auto window_to_image_filter =
            vtkSmartPointer<vtkWindowToImageFilter>::New();
        window_to_image_filter->SetInput(renWin);
        window_to_image_filter->SetScale(1); // image quality

        window_to_image_filter->ReadFrontBufferOff();
        window_to_image_filter->Update();

        writer->SetFileName(fn.c_str());
        writer->SetInputConnection(window_to_image_filter->GetOutputPort());
        writer->Write();
        return;
    }
}










int main(int argc, char* argv[])
{
    ifstream name_in_1("name.txt");
    //ifstream img_in("image_bound.txt");
    std::string filenum_1;
    //std::cout << "okkkkkk" << std::endl;

    while (name_in_1 >> filenum_1)
    {
        //break;
        int value;
        name_in_1 >> value;
        std::cout << value << std::endl;
        std::string file = "Files/SaveRaw";
        //std::string file;
        std::cout << file.append(filenum_1 + "_" + std::to_string(value)) << std::endl;
        vtkSmartPointer<vtkNamedColors> colors =
            vtkSmartPointer<vtkNamedColors>::New();
        std::array<unsigned char, 4> bkg{ {255, 255, 255, 255} };
        colors->SetColor("BkgColor", bkg.data());

        //
        vtkSmartPointer<vtkRenderer> aRenderer =
            vtkSmartPointer<vtkRenderer>::New();
        vtkSmartPointer<vtkRenderWindow> renWin =
            vtkSmartPointer<vtkRenderWindow>::New();
        renWin->AddRenderer(aRenderer);

        vtkSmartPointer<vtkRenderWindowInteractor> iren =
            vtkSmartPointer<vtkRenderWindowInteractor>::New();
        iren->SetRenderWindow(renWin);

        vtkSmartPointer<vtkMetaImageReader> reader =
            vtkSmartPointer<vtkMetaImageReader>::New();

        std::string loadfile = file;
        loadfile.append("/sample.mhd");

        std::cout << "loadfile:  " << loadfile.c_str();
        std::cout << std::endl;


        reader->SetFileName(loadfile.c_str());

        vtkSmartPointer<vtkMarchingCubes> boneExtractor =
            vtkSmartPointer<vtkMarchingCubes>::New();
        boneExtractor->SetInputConnection(reader->GetOutputPort());
        boneExtractor->SetValue(0, value);

        vtkSmartPointer<vtkStripper> boneStripper =
            vtkSmartPointer<vtkStripper>::New();
        boneStripper->SetInputConnection(boneExtractor->GetOutputPort());

        vtkSmartPointer<vtkPolyDataMapper> boneMapper =
            vtkSmartPointer<vtkPolyDataMapper>::New();
        boneMapper->SetInputConnection(boneStripper->GetOutputPort());
        boneMapper->ScalarVisibilityOff();

        vtkSmartPointer<vtkActor> bone =
            vtkSmartPointer<vtkActor>::New();
        bone->SetMapper(boneMapper);
        bone->GetProperty()->SetDiffuseColor(colors->GetColor3d("Ivory").GetData());

        aRenderer->AddActor(bone);
        aRenderer->ResetCamera();
        aRenderer->GetActiveCamera()->ParallelProjectionOn();
        std::cout << "pre" << std::endl;

        vtkSmartPointer<vtkSTLWriter> stlWriter =
            vtkSmartPointer<vtkSTLWriter>::New();

        std::string savefile = "befor_smooth_STL/";
        savefile.append(filenum_1 + "_" + std::to_string(value));
        savefile.append(".stl");


        std::cout << "savefile:  " << savefile.c_str();
        std::cout << std::endl;
        stlWriter->SetFileName(savefile.c_str());


        stlWriter->SetInputConnection(boneStripper->GetOutputPort());
        stlWriter->Write();
        std::cout << "after" << std::endl;
        //#########################################################################显示渲染模型################################################################
       /* aRenderer->SetBackground(colors->GetColor3d("BkgColor").GetData());
        renWin->SetSize(1500, 1500);
        renWin->Render();
        iren->Initialize();
        iren->Start();*/
        //#########################################################################显示渲染模型################################################################

    }

    ifstream name_in_2("name.txt");
    //ifstream img_in("image_bound.txt");
    std::string filenum_2;

    while (name_in_2 >> filenum_2)
    {
        //break;
        int value;
        name_in_2 >> value;

        std::string file = "befor_smooth_STL/";
        file.append(filenum_2 + "_" + std::to_string(value));
        file.append(".stl");
        std::cout << file << std::endl;



        // Read and display for verification
        vtkSmartPointer<vtkSTLReader> reader =
            vtkSmartPointer<vtkSTLReader>::New();
        reader->SetFileName(file.c_str());
        reader->Update();



        vtkSmartPointer<vtkSmoothPolyDataFilter> smoothFilter =
            vtkSmartPointer<vtkSmoothPolyDataFilter>::New();
        smoothFilter->SetInputConnection(reader->GetOutputPort());
        smoothFilter->SetNumberOfIterations(30);
        smoothFilter->SetRelaxationFactor(0.2);
        smoothFilter->FeatureEdgeSmoothingOff();
        smoothFilter->BoundarySmoothingOn();
        smoothFilter->Update();

        // Update normals on newly smoothed polydata
        vtkSmartPointer<vtkPolyDataNormals> normalGenerator = vtkSmartPointer<vtkPolyDataNormals>::New();
        normalGenerator->SetInputConnection(smoothFilter->GetOutputPort());
        normalGenerator->ComputePointNormalsOn();
        normalGenerator->ComputeCellNormalsOn();
        normalGenerator->Update();

        //vtkSmartPointer<vtkPolyDataMapper> inputMapper =
        //    vtkSmartPointer<vtkPolyDataMapper>::New();
        //inputMapper->SetInputConnection(reader->GetOutputPort());
        //vtkSmartPointer<vtkActor> inputActor =
        //    vtkSmartPointer<vtkActor>::New();
        //inputActor->SetMapper(inputMapper);

        vtkSmartPointer<vtkPolyDataMapper> smoothedMapper =
            vtkSmartPointer<vtkPolyDataMapper>::New();
        smoothedMapper->SetInputConnection(normalGenerator->GetOutputPort());
        vtkSmartPointer<vtkActor> smoothedActor =
            vtkSmartPointer<vtkActor>::New();
        smoothedActor->SetMapper(smoothedMapper);



        std::string savefile = "STL/";
        savefile.append(filenum_2 + "_" + std::to_string(value));
        savefile.append(".stl");
        //savefile.append(file);


        vtkSmartPointer<vtkSTLWriter> stlWriter =
            vtkSmartPointer<vtkSTLWriter>::New();
        stlWriter->SetFileName(savefile.c_str());
        stlWriter->SetInputConnection(normalGenerator->GetOutputPort());
        stlWriter->Write();


     

    }





    //ifstream gt_in("gt_bound.txt");
    ifstream img_in("image_bound.txt");
    std::string filenum;
    while (img_in >> filenum)
    {
        std::cout << filenum << std::endl;
        int value;
        img_in >> value;

        std::cout << filenum << std::endl;
        clock_t start, finish;
        start = clock();
        std::string inputFilename = "STL/";
        inputFilename.append(filenum + "_" + std::to_string(value));
        inputFilename.append(".stl");
        vtkSmartPointer<vtkSTLReader> reader =
            vtkSmartPointer<vtkSTLReader>::New();
        reader->SetFileName(inputFilename.c_str());
        reader->Update();
        double bounds[6];
        reader->GetOutput()->GetBounds(bounds);
        std::cout << bounds[0] << std::endl;
        std::cout << bounds[1] << std::endl;
        std::cout << bounds[2] << std::endl;
        std::cout << bounds[3] << std::endl;
        std::cout << bounds[4] << std::endl;
        std::cout << bounds[5] << std::endl;

        //定义一个平面
        vtkSmartPointer<vtkPlane> clipPlane_1 =
            vtkSmartPointer<vtkPlane>::New();


        vtkSmartPointer<vtkClipPolyData> clipper_1 =
            vtkSmartPointer<vtkClipPolyData>::New();


        vtkSmartPointer<vtkPolyDataMapper> superquadricMapper =
            vtkSmartPointer<vtkPolyDataMapper>::New();

        vtkSmartPointer<vtkActor> superquadricActor =
            vtkSmartPointer<vtkActor>::New();

        vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();

        vtkSmartPointer<vtkRenderWindow> renderWindow =
            vtkSmartPointer<vtkRenderWindow>::New();
        renderWindow->AddRenderer(renderer);
        renderWindow->SetSize(2000, 2000);

        vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
            vtkSmartPointer<vtkRenderWindowInteractor>::New();
        renderWindowInteractor->SetRenderWindow(renderWindow);
        renderer->GetActiveCamera()->ParallelProjectionOn();
        renderer->SetBackground(0, 0, 0);
        //clipper->SetInputConnection(reader->GetOutputPort());




        vtkSmartPointer<vtkOutlineFilter> outline =
            vtkSmartPointer<vtkOutlineFilter>::New();


        vtkSmartPointer<vtkPolyDataMapper> outlineMapper =
            vtkSmartPointer<vtkPolyDataMapper>::New();

        vtkSmartPointer<vtkActor> outlineActor =
            vtkSmartPointer<vtkActor>::New();

        //renderer->AddActor(outlineActor);
        outline->SetInputData(reader->GetOutput());
        outlineMapper->SetInputConnection(outline->GetOutputPort());
        outlineActor->SetMapper(outlineMapper);
        outlineActor->GetProperty()->SetColor(1, 1, 1);






        //float img_right = 426, img_left = 95, img_front = 27, img_back = 443, img_down = 236, img_up = 0;
        //float gt_right = 192, gt_left = 181, gt_front = 170, gt_back = 182, gt_down = 133, gt_up = 126;
        float img_right, img_left, img_front, img_back, img_down, img_up;
       // float gt_right, gt_left, gt_front, gt_back, gt_down, gt_up;
        //gt_in >> gt_right;
        //gt_in >> gt_left;
        //gt_in >> gt_front;
        //gt_in >> gt_back;
        //gt_in >> gt_down;
        // >> gt_up;

        img_in >> img_right;
        img_in >> img_left;
        img_in >> img_front;
        img_in >> img_back;
        img_in >> img_down;
        img_in >> img_up;


        //float plane_left = (bounds[1] - bounds[0]) / (img_right - img_left) * (gt_left - img_left) + bounds[0];
        float left_right_interval = (bounds[1] - bounds[0]) / (img_right - img_left);
        //float plane_right = (bounds[1] - bounds[0]) / (img_right - img_left) * (gt_right - img_left) + bounds[0];
        float front_back_interval = (bounds[3] - bounds[2]) / (img_back - img_front);

        //float plane_front = (bounds[3] - bounds[2]) / (img_back - img_front) * (img_back - gt_front) + bounds[2];
        //float plane_back = (bounds[3] - bounds[2]) / (img_back - img_front) * (img_back - gt_back) + bounds[2];
        float up_down_interval = (bounds[5] - bounds[4]) / (img_down - img_up);

        //float plane_up = (bounds[5] - bounds[4]) / (img_down - img_up) * (gt_up - img_up) + bounds[4];
       // float plane_down = (bounds[5] - bounds[4]) / (img_down - img_up) * (gt_down - img_up) + bounds[4];

        left_right_interval = left_right_interval;
        front_back_interval = front_back_interval;
        up_down_interval = up_down_interval;
        std::cout << img_right << "   " << img_left << "   " << img_front << "   " << img_back << "   " << img_down << "   " << img_up << std::endl;

        //std::cout << plane_left << "   " << plane_right << "   " << plane_front << "   " << plane_back << "   " << plane_up << "   " << plane_down << std::endl;



        //float plane[6] = { plane_left,plane_right,plane_front,plane_back,plane_up,plane_down };
        vtkSmartPointer<vtkProperty> backFaces =
            vtkSmartPointer<vtkProperty>::New();

        /*****************************************************************************************************************************************/
        int num = 0;
        for (float plane_left_slice = bounds[0]; plane_left_slice <= bounds[1]; plane_left_slice = plane_left_slice + left_right_interval)
        {
            //std::cout << "left" << std::endl;

            clipPlane_1->SetNormal(1, 0, 0);//法向量
            clipPlane_1->SetOrigin(plane_left_slice, 0.0, 0.0);
            clipper_1->SetInputConnection(reader->GetOutputPort());
            clipper_1->SetClipFunction(clipPlane_1);
            clipper_1->InsideOutOff();//法向量的反方向是inside


   


            superquadricMapper->SetInputConnection(clipper_1->GetOutputPort());
            superquadricActor->SetMapper(superquadricMapper);

            backFaces->SetSpecular(0.0);
            backFaces->SetDiffuse(0.0);
            backFaces->SetAmbient(1.0);
            backFaces->SetAmbientColor(1.0000, 0.3882, 0.2784);

            superquadricActor->SetBackfaceProperty(backFaces);


            renderer->AddActor(superquadricActor);
            renderer->AddActor(outlineActor);
            if (plane_left_slice == bounds[0])
            {

                superquadricActor->RotateX(90);
                outlineActor->RotateX(90);
                superquadricActor->RotateZ(-90);
                outlineActor->RotateZ(-90);
            }
            renderer->ResetCamera();
            renderWindow->Render();
            std::string imgname = "output/" + filenum + "_" + std::to_string(value) + "_" + "plane_left_" + std::to_string(num++) + ".jpg";
            WriteImage(imgname, renderWindow, false);
        }
        num = num - 1;


        /*****************************************************************************************************************************************/
        for (float plane_right_slice = bounds[1]; plane_right_slice >= bounds[0]; plane_right_slice = plane_right_slice - left_right_interval)
        {
            //std::cout << "right" << std::endl;
            clipPlane_1->SetNormal(1, 0, 0);//法向量
            clipPlane_1->SetOrigin(plane_right_slice, 0.0, 0.0);
            clipper_1->SetInputConnection(reader->GetOutputPort());
            clipper_1->SetClipFunction(clipPlane_1);
            clipper_1->InsideOutOn();//法向量的反方向是inside




            superquadricMapper->SetInputConnection(clipper_1->GetOutputPort());
            superquadricActor->SetMapper(superquadricMapper);

            backFaces->SetSpecular(0.0);
            backFaces->SetDiffuse(0.0);
            backFaces->SetAmbient(1.0);
            backFaces->SetAmbientColor(1.0000, 0.3882, 0.2784);

            superquadricActor->SetBackfaceProperty(backFaces);


            renderer->AddActor(superquadricActor);
            renderer->AddActor(outlineActor);
            if (plane_right_slice == bounds[1])
            {
                superquadricActor->RotateZ(90);
                outlineActor->RotateZ(90);
                superquadricActor->RotateZ(90);
                outlineActor->RotateZ(90);
            }
            renderer->ResetCamera();
            renderWindow->Render();
            std::string imgname = "output/" + filenum + "_" + std::to_string(value) + "_" + "plane_right_" + std::to_string(num--) + ".jpg";
            WriteImage(imgname, renderWindow, false);
        }

        /*****************************************************************************************************************************************/
        num = 0;
        for (float plane_front_slice = bounds[3]; plane_front_slice >= bounds[2]; plane_front_slice = plane_front_slice - front_back_interval)
        {
            //std::cout << "front" << std::endl;
            clipPlane_1->SetNormal(0, 1, 0);//法向量
            clipPlane_1->SetOrigin(0.0, plane_front_slice, 0.0);
            clipper_1->SetInputConnection(reader->GetOutputPort());
            clipper_1->SetClipFunction(clipPlane_1);
            clipper_1->InsideOutOn();//法向量的反方向是inside



            


            superquadricMapper->SetInputConnection(clipper_1->GetOutputPort());
            superquadricActor->SetMapper(superquadricMapper);

            backFaces->SetSpecular(0.0);
            backFaces->SetDiffuse(0.0);
            backFaces->SetAmbient(1.0);
            backFaces->SetAmbientColor(1.0000, 0.3882, 0.2784);

            superquadricActor->SetBackfaceProperty(backFaces);



            renderer->AddActor(superquadricActor);
            renderer->AddActor(outlineActor);
            if (plane_front_slice == bounds[3])
            {
                superquadricActor->RotateZ(-90);
                outlineActor->RotateZ(-90);
            }
            renderer->ResetCamera();
            renderWindow->Render();
            std::string imgname = "output/" + filenum + "_" + std::to_string(value) + "_" + "plane_front_" + std::to_string(num++) + ".jpg";
            WriteImage(imgname, renderWindow, false);
        }
        num = num - 1;

        /****************************************************************************************************************************************/


        for (float plane_back_slice = bounds[2]; plane_back_slice <= bounds[3]; plane_back_slice = plane_back_slice + front_back_interval)
        {
            //std::cout << "back" << std::endl;

            clipPlane_1->SetNormal(0, 1, 0);//法向量
            clipPlane_1->SetOrigin(0.0, plane_back_slice, 0.0);
            clipper_1->SetInputConnection(reader->GetOutputPort());
            clipper_1->SetClipFunction(clipPlane_1);
            clipper_1->InsideOutOff();//法向量的反方向是inside


   


            superquadricMapper->SetInputConnection(clipper_1->GetOutputPort());
            superquadricActor->SetMapper(superquadricMapper);

            backFaces->SetSpecular(0.0);
            backFaces->SetDiffuse(0.0);
            backFaces->SetAmbient(1.0);
            backFaces->SetAmbientColor(1.0000, 0.3882, 0.2784);

            superquadricActor->SetBackfaceProperty(backFaces);


            renderer->AddActor(superquadricActor);
            renderer->AddActor(outlineActor);
            if (plane_back_slice == bounds[2])
            {
                superquadricActor->RotateZ(180);
                outlineActor->RotateZ(180);
            }
            renderer->ResetCamera();
            renderWindow->Render();
            std::string imgname = "output/" + filenum + "_" + std::to_string(value) + "_" + "plane_back_" + std::to_string(num--) + ".jpg";
            WriteImage(imgname, renderWindow, false);
        }
        /*****************************************************************************************************************************************/

        num = 0;

        for (float plane_down_slice = bounds[4]; plane_down_slice <= bounds[5]; plane_down_slice = plane_down_slice + up_down_interval)
        {

            //std::cout << "down" << std::endl;
            clipPlane_1->SetNormal(0, 0, 1);//法向量
            clipPlane_1->SetOrigin(0.0, 0.0, plane_down_slice);
            clipper_1->SetInputConnection(reader->GetOutputPort());
            clipper_1->SetClipFunction(clipPlane_1);
            clipper_1->InsideOutOn();//法向量的反方向是inside
       


            superquadricMapper->SetInputConnection(clipper_1->GetOutputPort());
            superquadricActor->SetMapper(superquadricMapper);

            backFaces->SetSpecular(0.0);
            backFaces->SetDiffuse(0.0);
            backFaces->SetAmbient(1.0);
            backFaces->SetAmbientColor(1.0000, 0.3882, 0.2784);

            superquadricActor->SetBackfaceProperty(backFaces);


            renderer->AddActor(superquadricActor);
            renderer->AddActor(outlineActor);
            if (plane_down_slice == bounds[4])
            {

                superquadricActor->RotateZ(180);
                outlineActor->RotateZ(180);
                superquadricActor->RotateX(-90);
                outlineActor->RotateX(-90);
            }
            renderer->ResetCamera();
            renderWindow->Render();
            std::string imgname = "output/" + filenum + "_" + std::to_string(value) + "_" + "plane_down_" + std::to_string(num++) + ".jpg";
            WriteImage(imgname, renderWindow, false);
        }
        num = num - 1;

        /****************************************************************************************************************************************/
        //cout << bounds[6] << std::endl;
        cout << bounds[5] << std::endl;



        for (float plane_up_slice = bounds[5]; plane_up_slice >= bounds[4]; plane_up_slice = plane_up_slice - up_down_interval)
        {
            //std::cout << "up" << std::endl;
            //     std::cout << "plane_up_slice" << plane_up_slice << std::endl;
            clipPlane_1->SetNormal(0, 0, 1);//法向量
            clipPlane_1->SetOrigin(0.0, 0.0, plane_up_slice);
            clipper_1->SetInputConnection(reader->GetOutputPort());
            clipper_1->SetClipFunction(clipPlane_1);
            clipper_1->InsideOutOff();//法向量的反方向是inside
      


            superquadricMapper->SetInputConnection(clipper_1->GetOutputPort());
            superquadricActor->SetMapper(superquadricMapper);


            backFaces->SetSpecular(0.0);
            backFaces->SetDiffuse(0.0);
            backFaces->SetAmbient(1.0);
            backFaces->SetAmbientColor(1.0000, 0.3882, 0.2784);

            superquadricActor->SetBackfaceProperty(backFaces);

            renderer->AddActor(superquadricActor);
            renderer->AddActor(outlineActor);
            if (plane_up_slice == bounds[5])
            {
                superquadricActor->RotateX(90);
                outlineActor->RotateX(90);
                superquadricActor->RotateX(90);
                outlineActor->RotateX(90);
            }

            renderer->ResetCamera();
            renderWindow->Render();
            std::string imgname = "output/" + filenum + "_" + std::to_string(value) + "_" + "plane_up_" + std::to_string(num--) + ".jpg";
            WriteImage(imgname, renderWindow, false);
        }
        /*****************************************************************************************************************************************/





        finish = clock();
        double totaltime;
        totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
        std::cout << totaltime << std::endl;
        //renderWindowInteractor->Start();
        std::cout << "ok" << std::endl;
    }
    //std::cout << "okkkkkkk" << std::endl;
    return EXIT_SUCCESS;
}