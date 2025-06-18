from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from ...models import NhanKhau, TamTruTamVang
from ...forms.nhankhau_form import NhanKhauForm, TamTruTamVangForm, TamTruForm
from ...utils import cap_nhat_trang_thai_tamtru_tamvang

#----------------------------------------Quản lý nhân khẩu-----------------------------
@login_required
def quanly_nhankhau(request):
    cap_nhat_trang_thai_tamtru_tamvang()
    query = request.GET.get('q', '').strip()
    if query:
        nhan_khau_list = NhanKhau.objects.filter(
            Q(ho_ten__icontains=query) |
            Q(ma_can_cuoc__icontains=query) |
            Q(so_dien_thoai__icontains=query)
        ).order_by('ho_ten')
    else:
        nhan_khau_list = NhanKhau.objects.all().order_by('ho_ten')

    paginator = Paginator(nhan_khau_list, 10)
    page_number = request.GET.get('page')
    nhan_khau_list = paginator.get_page(page_number)

    return render(request, 'quanly/nhankhau/quanly_nhankhau.html', {
        'nhan_khau_list': nhan_khau_list,
        'query': query,
    })

@login_required
def them_nhankhau(request):
    if request.method == 'POST':
        form = NhanKhauForm(request.POST)
        if form.is_valid():
            nhankhau = form.save()
            if nhankhau.quan_he_voi_chu_ho == 'Chủ hộ':
                ho_khau = nhankhau.ho_khau
                ho_khau.chu_ho = nhankhau
                ho_khau.save()
            messages.success(request, 'Thêm nhân khẩu thành công!')
            return redirect('quanly_nhankhau')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin!')
    else:
        form = NhanKhauForm()
    return render(request, 'quanly/nhankhau/them_nhankhau.html', {'form': form})

@login_required
def sua_nhankhau(request, pk):
    nhankhau = get_object_or_404(NhanKhau, pk=pk)
    if request.method == 'POST':
        form = NhanKhauForm(request.POST, instance=nhankhau)
        if form.is_valid():
            nhankhau = form.save()
            if nhankhau.quan_he_voi_chu_ho == 'Chủ hộ':
                ho_khau = nhankhau.ho_khau
                ho_khau.chu_ho = nhankhau
                ho_khau.save()
            messages.success(request, 'Cập nhật nhân khẩu thành công!')
            return redirect('quanly_nhankhau')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin!')
    else:
        form = NhanKhauForm(instance=nhankhau)
    return render(request, 'quanly/nhankhau/sua_nhankhau.html', {
        'form': form,
        'nhankhau': nhankhau
    })

@login_required
def chitiet_nhankhau(request, pk):
    nhan_khau = get_object_or_404(NhanKhau, pk=pk)
    tam_tru_tam_vang = None
    if nhan_khau.trang_thai in ['Tạm trú', 'Tạm vắng']:
        tam_tru_tam_vang = TamTruTamVang.objects.filter(nhan_khau=nhan_khau).first()

    return render(request, 'quanly/nhankhau/chitiet_nhankhau.html', {
        'nhankhau': nhan_khau,
        'tam_tru_tam_vang': tam_tru_tam_vang
    })

@login_required
def xoa_nhankhau(request, pk):
    nhan_khau = get_object_or_404(NhanKhau, pk=pk)
    if request.method == 'POST':
        nhan_khau.delete()
        messages.success(request, 'Xóa nhân khẩu thành công!')
        return redirect('quanly_nhankhau')
    return render(request, 'quanly/nhankhau/xoa_nhankhau.html', {'nhan_khau': nhan_khau})

@login_required
def them_tamtru(request):
    if request.method == 'POST':
        form = TamTruForm(request.POST)
        if form.is_valid():
            nhankhau = form.save()
            return redirect('them_tamtru_info', nhankhau_id=nhankhau.id)
    else:
        form = TamTruForm()

    return render(request, 'quanly/nhankhau/them_tamtru.html', {'form': form})

@login_required
def chon_nhankhau_tamvang(request):
    query = request.GET.get('q', '')
    nhan_khau_list = NhanKhau.objects.exclude(trang_thai='Tạm trú')
    if query:
        nhan_khau_list = nhan_khau_list.filter(
            Q(ho_ten__icontains=query) |
            Q(ma_can_cuoc__icontains=query)
        )
    return render(request, 'quanly/nhankhau/chon_nhankhau_tamvang.html', {
        'nhan_khau_list': nhan_khau_list,
        'query': query
    })

@login_required
def dang_ky_tam_vang(request, nhankhau_id):
    nhankhau = get_object_or_404(NhanKhau, id=nhankhau_id)
    if request.method == 'POST':
        form = TamTruTamVangForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.nhan_khau = nhankhau
            record.loai = 'Tạm vắng'
            record.save()
            nhankhau.trang_thai = 'Tạm vắng'
            nhankhau.save()
            messages.success(request, 'Đăng ký tạm vắng thành công!')
            return redirect('quanly_nhankhau')
    else:
        form = TamTruTamVangForm()
    return render(request, 'quanly/nhankhau/tamtru_tamvang.html', {
        'form': form,
        'nhankhau': nhankhau,
        'loai': 'Tạm vắng'
    })

@login_required
def them_tamtru(request):
    if request.method == 'POST':
        form = TamTruForm(request.POST)
        if form.is_valid():
            nhankhau = form.save()  # Save the NhanKhau object
            # Chuyển hướng sau khi lưu thành công
            return redirect('tamtru_tamvang', nhankhau_id=nhankhau.id)  # Đảm bảo rằng URL tên đúng
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin!')
    else:
        form = TamTruForm()

    return render(request, 'quanly/nhankhau/them_tamtru.html', {'form': form})

@login_required
def them_tamtru_info(request, nhankhau_id):
    # Get the NhanKhau object using the provided ID
    nhankhau = get_object_or_404(NhanKhau, pk=nhankhau_id)
    
    if request.method == 'POST':
        # Process the TamTruTamVang form to handle the temporary residence information
        tamtru_form = TamTruTamVangForm(request.POST)
        if tamtru_form.is_valid():
            # Save the temporary residence information (TamTruTamVang)
            tamtru = tamtru_form.save(commit=False)
            tamtru.nhan_khau = nhankhau  # Link the temporary stay with the NhanKhau
            tamtru.loai = 'Tạm trú'  # Set the type to 'Tạm trú'
            tamtru.save()

            # Update the NhanKhau's status to 'Tạm trú'
            nhankhau.trang_thai = 'Tạm trú'
            nhankhau.save()

            messages.success(request, 'Đã đăng ký tạm trú thành công!')
            return redirect('quanly_nhankhau')  # Redirect back to the list of NhanKhau after saving
    else:
        tamtru_form = TamTruTamVangForm()

    return render(request, 'quanly/nhankhau/tamtru_tamvang.html', {
        'form': tamtru_form,
        'nhankhau': nhankhau,
        'loai': 'Tạm trú',
    })
