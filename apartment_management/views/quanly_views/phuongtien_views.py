from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ...models import HoKhau, PhuongTien
from ...forms.phuongtien_form import PhuongTienForm
from ...views.nguoidung_views import role_required

def cap_nhat_so_xe(ho_khau):
    xe_may = ho_khau.phuongtien_set.filter(loai_phuong_tien='Xe máy').count()
    o_to = ho_khau.phuongtien_set.filter(loai_phuong_tien='Ô tô').count()
    ho_khau.so_xe_may = xe_may
    ho_khau.so_o_to = o_to
    ho_khau.save()

@login_required
@role_required('Quản lý')
def quanly_phuongtien(request):
    query = request.GET.get('q', '').strip() 
    ho_khau_list = HoKhau.objects.all().prefetch_related('phuongtien_set')  

    if query:
        ho_khau_list = ho_khau_list.filter(
            Q(so_can_ho__icontains=query) | 
            Q(toa_nha__icontains=query) |  
            Q(phuongtien__bien_so__icontains=query) |
            Q(phuongtien__loai_phuong_tien__icontains=query) |  
            Q(phuongtien__mo_ta__icontains=query) 
        ).distinct() 

    return render(request, 'quanly/phuongtien/quanly_phuongtien.html', {
        'ho_khau_list': ho_khau_list,
        'query': query,
    })



@login_required
@role_required('Quản lý')
def chitiet_phuongtien(request, ho_id):
    ho_khau = get_object_or_404(HoKhau, id=ho_id)
    phuong_tien_list = ho_khau.phuongtien_set.all()

    return render(request, 'quanly/phuongtien/chitiet_phuongtien.html', {
        'ho_khau': ho_khau,
        'phuong_tien_list': phuong_tien_list,
    })

@login_required
@role_required('Quản lý')
def them_phuongtien(request, ho_id):
    ho_khau = get_object_or_404(HoKhau, id=ho_id)
    if request.method == 'POST':
        form = PhuongTienForm(request.POST)
        if form.is_valid():
            phuong_tien = form.save(commit=False)
            phuong_tien.ho_khau = ho_khau
            phuong_tien.save()
            cap_nhat_so_xe(ho_khau)  # Cập nhật lại số lượng phương tiện cho hộ khẩu
            messages.success(request, 'Thêm phương tiện thành công!')
            return redirect('chitiet_phuongtien', ho_id=ho_khau.id)
    else:
        form = PhuongTienForm(initial={'ho_khau': ho_khau})  # tiện mở rộng

    return render(request, 'quanly/phuongtien/them_phuongtien.html', {
        'ho_khau': ho_khau,
        'form': form,
    })


@login_required
@role_required('Quản lý')
def sua_phuongtien(request, phuongtien_id):
    phuong_tien = get_object_or_404(PhuongTien, id=phuongtien_id)
    ho_khau = phuong_tien.ho_khau
    if request.method == 'POST':
        form = PhuongTienForm(request.POST, instance=phuong_tien)
        if form.is_valid():
            form.save()
            cap_nhat_so_xe(ho_khau)  # Cập nhật lại số lượng phương tiện cho hộ khẩu
            messages.success(request, 'Cập nhật phương tiện thành công!')
            return redirect('chitiet_phuongtien', ho_id=ho_khau.id)
    else:
        form = PhuongTienForm(instance=phuong_tien)

    return render(request, 'quanly/phuongtien/sua_phuongtien.html', {
        'form': form,
        'phuong_tien': phuong_tien,
    })

@login_required
@role_required('Quản lý')
def xoa_phuongtien(request, phuongtien_id):
    phuong_tien = get_object_or_404(PhuongTien, id=phuongtien_id)
    ho_khau = phuong_tien.ho_khau
    
    if request.method == 'POST':
        phuong_tien.delete() 
        cap_nhat_so_xe(ho_khau)  
        messages.success(request, 'Xóa phương tiện thành công!')
        return redirect('chitiet_phuongtien', ho_id=ho_khau.id)  
    
    return render(request, 'quanly/phuongtien/xoa_phuongtien.html', {
        'phuong_tien': phuong_tien,
        'ho_khau': ho_khau,
    })

