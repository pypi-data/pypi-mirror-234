#include <pybind11/pybind11.h>
#include <pybind11/iostream.h>
#include <pybind11/numpy.h>
#include <map>

/* Compile using
c++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` perffuncs.cpp -o perffuncs`python3-config --extension-suffix`
*/

namespace py = pybind11;

py::array_t<double> diffusion(py::array_t<double> dydt, py::array_t<double> y0, py::array_t<bool> bool_array, py::array_t<double> neighbors, double alpha, int n_neighbors){
    py::buffer_info buf4 = dydt.request();
    py::buffer_info buf1 = y0.request();
    py::buffer_info buf2 = bool_array.request();
    py::buffer_info buf3 = neighbors.request();

    double *ptr1 = (double *) buf1.ptr,
           *ptr3 = (double *) buf3.ptr,
           *ptr4 = (double *) buf4.ptr;
    bool *ptr2 = (bool *) buf2.ptr;

    int pos = 0;
    for (int i = 0; i < buf1.shape[0]; i++){
      // py::print(ptr2[i]);
      if (ptr2[i] == true){
        for (int j=0; j < n_neighbors; j++){
          pos = ptr3[i*n_neighbors + j];
          if (pos != -1){
            ptr4[i] += (ptr1[pos] - ptr1[i])/n_neighbors * alpha;
          }
        }
      }
    }
    return dydt;
}

py::array_t<double> diffusion_nonavg(py::array_t<double> dydt, py::array_t<double> y0, py::array_t<bool> bool_array, py::array_t<double> neighbors, double alpha, int n_neighbors){
    py::buffer_info buf4 = dydt.request();
    py::buffer_info buf1 = y0.request();
    py::buffer_info buf2 = bool_array.request();
    py::buffer_info buf3 = neighbors.request();

    double *ptr1 = (double *) buf1.ptr,
           *ptr3 = (double *) buf3.ptr,
           *ptr4 = (double *) buf4.ptr;
    bool *ptr2 = (bool *) buf2.ptr;

    int pos = 0;
    for (int i = 0; i < buf1.shape[0]; i++){
      // py::print(ptr2[i]);
      if (ptr2[i] == true){
        for (int j=0; j < n_neighbors; j++){
          pos = ptr3[i*n_neighbors + j];
          if (pos != -1){
            ptr4[i] += (ptr1[pos] - ptr1[i]) * alpha;
          }
        }
      }
    }
    return dydt;
}

py::array_t<double> active_transport(py::array_t<double> dydt, py::array_t<double> y0, py::array_t<bool> bool_array, py::array_t<double> neighbors, double alpha, int n_neighbors){
    py::buffer_info buf4 = dydt.request();
    py::buffer_info buf1 = y0.request();
    py::buffer_info buf2 = bool_array.request();
    py::buffer_info buf3 = neighbors.request();

    double *ptr1 = (double *) buf1.ptr,
           *ptr3 = (double *) buf3.ptr,
           *ptr4 = (double *) buf4.ptr;
    bool *ptr2 = (bool *) buf2.ptr;

    int pos = 0;
    for (int i = 0; i < buf1.shape[0]; i++){
      // py::print(ptr2[i]);
      if (ptr2[i] == true){
        for (int j=0; j < n_neighbors; j++){
          pos = ptr3[i*n_neighbors + j];
          if (pos != -1){
            double diff = (ptr1[pos] - ptr1[i]) * alpha;
            if (diff < 0){
              ptr4[i] += diff;
              ptr4[pos] -= diff;
            }
          }
        }
      }
    }
    return dydt;
}


PYBIND11_MODULE(_perffuncs, m) {
    m.doc() = "High-performance functions"; // optional module docstring
    m.def("diffusion", &diffusion, "Description");
    m.def("diffusion_nonavg", &diffusion_nonavg, "Description");
    m.def("active_transport", &active_transport, "Description");
}
