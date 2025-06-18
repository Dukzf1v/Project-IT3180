from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from ...models import HoKhau, NhanKhau
from ...forms.hokhau_form import HoKhauForm
from ..nguoidung_views import role_required

#---------------------------------------- Quản lý hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def quanly_hokhau(request):
    query = request.GET.get('q', '').strip()
    ho_khau_list = HoKhau.objects.annotate(
        tong_thanh_vien=Count('nhankhau') 
    ).order_by('so_can_ho')

    if query:
        ho_khau_list = ho_khau_list.filter(
            Q(so_can_ho__icontains=query) |
            Q(toa_nha__icontains=query) |
            Q(chu_ho__ho_ten__icontains=query)
        )

    return render(request, 'quanly/hokhau/quanly_hokhau.html', {
        'ho_khau_list': ho_khau_list,
        'query': query,
    })
#---------------------------------------- Chi tiết hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def chitiet_hokhau(request, ho_id):
    ho = get_object_or_404(HoKhau, id=ho_id)
    thanh_vien_list = ho.nhankhau_set.all()
    return render(request, 'quanly/hokhau/chitiet_hokhau.html', {
        'ho': ho,
        'thanh_vien_list': thanh_vien_list,
    })

#---------------------------------------- Thêm hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def them_hokhau(request):
    if request.method == 'POST':
        form = HoKhauForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm hộ khẩu thành công!')
            return redirect('quanly_hokhau')
    else:
        form = HoKhauForm()
    
    return render(request, 'quanly/hokhau/them_hokhau.html', {'form': form})

#---------------------------------------- Sửa hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def sua_hokhau(request, ho_id):
    ho = get_object_or_404(HoKhau, id=ho_id)
    if request.method == 'POST':
        form = HoKhauForm(request.POST, instance=ho)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật hộ khẩu thành công!')
            return redirect('chitiet_hokhau', ho_id=ho.id)  
    else:
        form = HoKhauForm(instance=ho)

    return render(request, 'quanly/hokhau/sua_hokhau.html', {'form': form, 'ho': ho})

#---------------------------------------- Xóa hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
@require_http_methods(["POST"])
def xoa_hokhau(request, ho_id):
    ho = get_object_or_404(HoKhau, id=ho_id)
    ho.delete()
    messages.success(request, 'Đã xóa hộ khẩu.')
    return redirect('quanly_hokhau')
#---------------------------------------- Chuyển hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def chuyen_hokhau(request, ho_id):
    ho_cu = get_object_or_404(HoKhau, id=ho_id)
    
    ho_moi_list = HoKhau.objects.annotate(
        so_thanh_vien=Count('nhankhau', filter=Q(nhankhau__trang_thai='Đang sinh sống'))).exclude(id=ho_cu.id) 
    ho_moi_list = ho_moi_list.filter(so_thanh_vien=0) 

    if request.method == 'POST':
        ho_moi_id = request.POST.get('ho_khau_moi')
        ho_moi = get_object_or_404(HoKhau, id=ho_moi_id)

        for nhan_khau in ho_cu.nhankhau_set.all():
            nhan_khau.ho_khau = ho_moi
            nhan_khau.save()

        ho_cu.chu_ho = None
        ho_cu.so_xe_may = 0
        ho_cu.so_o_to = 0
        ho_cu.save()

        ho_cu.trang_thai = 'Đã rời đi'
        ho_cu.save()

        ho_moi.trang_thai = 'Đang ở'
        ho_moi.save()

        messages.success(request, 'Chuyển hộ khẩu thành công.')
        return redirect('quanly_hokhau')

    return render(request, 'quanly/hokhau/chuyen_hokhau.html', {
        'ho_cu': ho_cu,
        'ho_moi_list': ho_moi_list 
    })
#--------------------------------------- Tách hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def tach_hokhau(request, ho_id):
    ho_cu = get_object_or_404(HoKhau, id=ho_id)
    thanh_vien_list = ho_cu.nhankhau_set.all()

    ho_moi_list = HoKhau.objects.filter(nhankhau__isnull=True)

    if request.method == 'POST':
        so_can_ho_moi = request.POST.get('so_can_ho')
        ids_thanh_vien = request.POST.getlist('thanh_vien_ids')

        if not so_can_ho_moi or not ids_thanh_vien:
            messages.error(request, 'Vui lòng chọn hộ khẩu mới và các thành viên muốn chuyển.')
            return redirect('tach_hokhau', ho_id=ho_id)

        ho_moi = get_object_or_404(HoKhau, so_can_ho=so_can_ho_moi)

        for tv_id in ids_thanh_vien:
            thanh_vien = NhanKhau.objects.get(id=tv_id)
            thanh_vien.ho_khau = ho_moi
            thanh_vien.save()

        chu_ho_moi = None
        for tv_id in ids_thanh_vien:
            thanh_vien = NhanKhau.objects.get(id=tv_id)
            if thanh_vien.quan_he_voi_chu_ho == 'Chủ hộ':
                chu_ho_moi = thanh_vien
                break

        if chu_ho_moi:
            ho_moi.chu_ho = chu_ho_moi
            ho_moi.save()

        if not chu_ho_moi:
            ho_moi.chu_ho = None
            ho_moi.save()

        ho_cu.chu_ho = None
        ho_cu.save()

        ho_cu.trang_thai = 'Đã rời đi'
        ho_cu.save()

        messages.success(request, f'Tách hộ thành công sang căn hộ {ho_moi.so_can_ho}.')
        return redirect('quanly_hokhau')

    return render(request, 'quanly/hokhau/tach_hokhau.html', {
        'ho': ho_cu,
        'thanh_vien_list': thanh_vien_list,
        'ho_moi_list': ho_moi_list,
    })

#---------------------------------------- Nhập hộ khẩu -----------------------------------------------
@login_required
@role_required('Quản lý')
def nhap_hokhau(request, ho_id):
    ho = get_object_or_404(HoKhau, id=ho_id)
    nhan_khau_khac = NhanKhau.objects.exclude(ho_khau=ho).filter(trang_thai='Đang sinh sống')

    if request.method == 'POST':
        ids_nhan_khau = request.POST.getlist('nhan_khau_ids')
        if not ids_nhan_khau:
            messages.error(request, 'Vui lòng chọn nhân khẩu để chuyển về hộ.')
            return redirect('nhap_hokhau', ho_id=ho.id)

        for nk_id in ids_nhan_khau:
            nk = NhanKhau.objects.get(id=nk_id)
            nk.ho_khau = ho
            nk.save()
        messages.success(request, f'Chuyển nhân khẩu về hộ {ho.so_can_ho} thành công.')
        return redirect('chitiet_hokhau', ho_id=ho.id)

    return render(request, 'quanly/hokhau/nhap_hokhau.html', {
        'ho': ho,
        'nhan_khau_khac': nhan_khau_khac,
    })