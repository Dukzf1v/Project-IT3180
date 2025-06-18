"""
URL configuration for BlueMoon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.shortcuts import redirect
from apartment_management.views import nguoidung_views
from apartment_management.views.ketoan_views import donggop_views, khoanthu_views
from apartment_management.views.quanly_views import hokhau_views, nhankhau_views, phuongtien_views

urlpatterns = [
    path('login/', nguoidung_views.login_view, name='login'),
    path('', lambda request: redirect('login')),
    path('logout/', nguoidung_views.logout_view, name='logout'),

    path('dashboard/quanly/', nguoidung_views.quanly_dashboard, name='quanly_dashboard'),
    path('dashboard/ketoan/', nguoidung_views.ketoan_dashboard, name='ketoan_dashboard'),

    path('quanly_nguoidung/', nguoidung_views.quanly_nguoidung, name='quanly_nguoidung'),
    path('them_nguoidung/', nguoidung_views.them_nguoidung, name='them_nguoidung'),
    path('sua_nguoidung/<int:user_id>/', nguoidung_views.sua_nguoidung, name='sua_nguoidung'),
    path('xoa_nguoidung/<int:user_id>/', nguoidung_views.xoa_nguoidung, name='xoa_nguoidung'),

    path('chitiet_hoso/', nguoidung_views.chitiet_hoso, name='chitiet_hoso'),  
    path('sua_hoso/', nguoidung_views.sua_hoso, name='sua_hoso'),
    path('thaydoi_matkhau/', nguoidung_views.thaydoi_matkhau, name='thaydoi_matkhau'),

    path('quanly/quan-ly-nhan-khau/', nhankhau_views.quanly_nhankhau, name='quanly_nhankhau'),
    path('quanly/them-nhan-khau/', nhankhau_views.them_nhankhau, name='them_nhankhau'),
    path('quanly/nhan-khau/<int:pk>/', nhankhau_views.chitiet_nhankhau, name='chitiet_nhankhau'),
    path('quanly/ho-khau/them/', hokhau_views.them_hokhau, name='them_hokhau'),
    path('quanly/nhan-khau/sua/<int:pk>/', nhankhau_views.sua_nhankhau, name='sua_nhankhau'),
    path('quanly/nhan-khau/xoa/<int:pk>/', nhankhau_views.xoa_nhankhau, name='xoa_nhankhau'),
    path('nhan-khau/them-tamtru/', nhankhau_views.them_tamtru, name='them_tamtru'),
    path('chon-tam-vang/', nhankhau_views.chon_nhankhau_tamvang, name='chon_nhankhau_tamvang'),
    path('nhan-khau/<int:nhankhau_id>/tam-vang/', nhankhau_views.dang_ky_tam_vang, name='tamvang'),
    path('nhan-khau/them-tam-tru/', nhankhau_views.them_tamtru, name='them_tamtru'),
    path('nhan-khau/<int:nhankhau_id>/them-tam-tru-info/', nhankhau_views.them_tamtru_info, name='tamtru_tamvang'),


    path('quanly/ho-khau/', hokhau_views.quanly_hokhau, name='quanly_hokhau'),
    path('quanly/ho-khau/<int:ho_id>/', hokhau_views.chitiet_hokhau, name='chitiet_hokhau'),
    path('quanly/ho-khau/sua/<int:ho_id>/', hokhau_views.sua_hokhau, name='sua_hokhau'),
    path('quanly/ho-khau/xoa/<int:ho_id>/', hokhau_views.xoa_hokhau, name='xoa_hokhau'),
    path('quanly/ho-khau/chuyen/<int:ho_id>/', hokhau_views.chuyen_hokhau, name='chuyen_hokhau'),
    path('quanly/ho-khau/tach/<int:ho_id>/', hokhau_views.tach_hokhau, name='tach_hokhau'),
    path('quanly/nhap-hokhau/<int:ho_id>/', hokhau_views.nhap_hokhau, name='nhap_hokhau'),

    path('quanly/phuong-tien/', phuongtien_views.quanly_phuongtien, name='quanly_phuongtien'),
    path('quanly/phuong-tien/<int:ho_id>/', phuongtien_views.chitiet_phuongtien, name='chitiet_phuongtien'),
    path('quanly/phuong-tien/<int:ho_id>/them/', phuongtien_views.them_phuongtien, name='them_phuongtien'),
    path('quanly/phuong-tien/<int:phuongtien_id>/sua/', phuongtien_views.sua_phuongtien, name='sua_phuongtien'),
    path('quanly/phuong-tien/<int:phuongtien_id>/xoa/', phuongtien_views.xoa_phuongtien, name='xoa_phuongtien'),

    path('ketoan/khoanthu/', khoanthu_views.quanly_khoanthu, name='quanly_khoanthu'),
    path('chi-tiet-phi/<int:ho_khau_id>/', khoanthu_views.chi_tiet_phi, name='chi_tiet_phi'),
    path('ketoan/ho-khau/<int:ho_khau_id>/cap-nhat-phi-sinh-hoat/', khoanthu_views.cap_nhat_phi_sinh_hoat, name='cap_nhat_phi_sinh_hoat'),
    path('ketoan/thong-ke/', khoanthu_views.thong_ke_khoan_phi, name='thong_ke_khoan_phi'),
    path('xac-nhan-thanh-toan/<int:ho_khau_id>/', khoanthu_views.xac_nhan_thanh_toan, name='xac_nhan_thanh_toan'),
    path('cap-nhat-phi-sinh-hoat/', khoanthu_views.cap_nhat_phi_sinh_hoat, name='cap_nhat_phi_sinh_hoat'),
    path('thong-ke-phi-dich-vu/', khoanthu_views.thong_ke_phi_dich_vu, name='thong_ke_phi_dich_vu'),
    path('thong-ke-phi-quan-ly/', khoanthu_views.thong_ke_phi_quan_ly, name='thong_ke_phi_quan_ly'),
    path('thong-ke-phi-gui-xe/', khoanthu_views.thong_ke_phi_gui_xe, name='thong_ke_phi_gui_xe'),
    path('thong-ke-phi-sinh-hoat/', khoanthu_views.thong_ke_phi_sinh_hoat, name='thong_ke_phi_sinh_hoat'),
    path('chi-tiet-phi-sinh-hoat/<int:ho_khau_id>/', khoanthu_views.chi_tiet_phi_sinh_hoat, name='chi_tiet_phi_sinh_hoat'),

    path('thong-ke-dong-gop/', donggop_views.thong_ke_dong_gop, name='thong_ke_dong_gop'),
    path('chi-tiet-dong-gop/<str:ten_phi>/', donggop_views.chi_tiet_dong_gop, name='chi_tiet_dong_gop'),
    path('them-dong-gop/', donggop_views.them_dong_gop, name='them_dong_gop'),
    path('sua-dong-gop/<str:id>/', donggop_views.sua_dong_gop, name='sua_dong_gop'),  # Sửa khoản đóng góp
    path('xoa-dong-gop/<str:id>/', donggop_views.xoa_dong_gop, name='xoa_dong_gop'),  # Xóa khoản đóng góp
    path('sua-dong-gop-ho/<int:id>/', donggop_views.sua_dong_gop_ho, name='sua_dong_gop_ho'),  # Sửa đóng góp của hộ gia đình
    path('xoa-dong-gop-ho/<int:id>/', donggop_views.xoa_dong_gop_ho, name='xoa_dong_gop_ho'),  # Xóa đóng góp của hộ gia đình
    path('them-dong-gop-ho/<str:ten_phi>/', donggop_views.them_dong_gop_ho, name='them_dong_gop_ho'),  # Thêm đóng góp cho hộ gia đình
]

