from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.views.decorators.cache import never_cache
import secrets
import string
import re
from django.db.models import Count
from django.db import transaction
from ..models import NguoiDung, User, HoKhau, NhanKhau, DongGopPhi
from ..forms.suahoso_form import SuaHoSoForm
from ..forms.suanguoidung_form import SuaNguoiDungForm
from django.utils import timezone

PHONE_REGEX = r'^[0-9]{10,15}$'


# -------------------- Decorator for Role-Based Access Control ------------------------
def role_required(required_role):
    """
    Decorator to check if the user has the required role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                nguoi_dung = getattr(request.user, 'nguoidung', None)
                if nguoi_dung and nguoi_dung.vai_tro == required_role:
                    return view_func(request, *args, **kwargs)
            return redirect('login')  
        return _wrapped_view
    return decorator


# -------------------- Authentication Views ---------------------------
@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                nguoi_dung = NguoiDung.objects.get(user=user)
                if nguoi_dung.vai_tro == 'Quản lý':
                    return redirect('quanly_dashboard')
                elif nguoi_dung.vai_tro == 'Kế toán':
                    return redirect('ketoan_dashboard')
                else:
                    messages.error(request, "Không xác định được vai trò người dùng.")
            except NguoiDung.DoesNotExist:
                messages.error(request, "Không tìm thấy thông tin người dùng.")
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
        
        return redirect('login')  

    return render(request, 'nguoidung/login.html')

# -------------------- Logout View ---------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 


# -------------------- Quan ly nguoi dung ---------------------------
@login_required
@role_required('Quản lý')
def quanly_nguoidung(request):
    users = User.objects.select_related('nguoidung').all().order_by('-date_joined')
    
    user_list = []
    stt = 1  # Start counting from 1
    for user in users:
        try:
            nguoi_dung = user.nguoidung
            user_list.append({
                'stt': stt,
                'id': user.id,
                'username': user.username,
                'password': user.password,  # Mật khẩu (mã hóa)
                'ho_ten': f"{user.last_name} {user.first_name}".strip(),
                'email': user.email,
                'so_dien_thoai': nguoi_dung.so_dien_thoai,
                'vai_tro': nguoi_dung.vai_tro,
            })
            stt += 1 
        except NguoiDung.DoesNotExist:
            continue
            
    context = {'users': user_list}
    return render(request, 'nguoidung/quanly_nguoidung.html', context)


# -------------------- Create New User ---------------------------

@login_required
@role_required('Quản lý')
def them_nguoidung(request):
    if request.method == 'POST':
        try:
            ho_ten = request.POST.get('ho_ten', '').strip()
            email = request.POST.get('email', '').strip()
            ten_dang_nhap = request.POST.get('ten_dang_nhap', '').strip()
            so_dien_thoai = request.POST.get('so_dien_thoai', '').strip()
            vai_tro = request.POST.get('vai_tro', '').strip()

            if not all([ho_ten, email, ten_dang_nhap, so_dien_thoai, vai_tro]):
                messages.error(request, 'Vui lòng điền đầy đủ thông tin')
                return redirect('them_nguoidung')

            if User.objects.filter(username=ten_dang_nhap).exists():
                messages.error(request, 'Tên đăng nhập đã tồn tại!')
                return redirect('them_nguoidung')

            if not re.match(PHONE_REGEX, so_dien_thoai):
                messages.error(request, 'Số điện thoại không hợp lệ. Vui lòng nhập từ 10 đến 15 chữ số.')
                return redirect('them_nguoidung')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email đã được sử dụng!')
                return redirect('them_nguoidung')

            # Tạo mật khẩu ngẫu nhiên
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for _ in range(secrets.choice(range(8, 13))))

            ho_ten_parts = ho_ten.split()
            last_name = ' '.join(ho_ten_parts[:-1]) if len(ho_ten_parts) > 1 else ''
            first_name = ho_ten_parts[-1] if ho_ten_parts else ''

            with transaction.atomic():
                user = User.objects.create_user(
                    username=ten_dang_nhap,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                NguoiDung.objects.create(
                    user=user,
                    ho_ten=ho_ten,
                    email=email,
                    vai_tro=vai_tro,
                    so_dien_thoai=so_dien_thoai
                )

            messages.success(request, f'Tạo tài khoản thành công! Mật khẩu mặc định là: {password}')
            return redirect('quanly_nguoidung')

        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            return redirect('them_nguoidung')

    return render(request, 'nguoidung/them_nguoidung.html')

# -------------------- Change Password ---------------------------

@login_required
def thaydoi_matkhau(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Mật khẩu đã được thay đổi thành công.')
            return redirect('chitiet_hoso') 
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin.')
            for field in form:
                for error in field.errors:
                    messages.error(request, error) 

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'nguoidung/thaydoi_matkhau.html', {'form': form})


# Xem thông tin hồ sơ
@login_required
def chitiet_hoso(request):
    try:
        nguoi_dung = request.user.nguoidung
    except NguoiDung.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin người dùng.")
        return redirect('quanly_dashboard')

    return render(request, 'nguoidung/chitiet_hoso.html', {'nguoi_dung': nguoi_dung})


# Sửa thông tin cá nhân
@login_required
def sua_hoso(request):
    try:
        nguoi_dung = request.user.nguoidung
    except NguoiDung.DoesNotExist:
        messages.error(request, "Không tìm thấy thông tin người dùng")
        return redirect('quanly_dashboard')

    if request.method == 'POST':
        form = SuaHoSoForm(request.POST, instance=nguoi_dung)
        if form.is_valid():
            so_dien_thoai = form.cleaned_data.get('so_dien_thoai', '')
            if not re.match(PHONE_REGEX, so_dien_thoai):
                messages.error(request, 'Số điện thoại không hợp lệ. Vui lòng nhập từ 10 đến 15 chữ số.')
                return render(request, 'nguoidung/sua_hoso.html', {'form': form})

            ho_ten = form.cleaned_data.get('ho_ten', '').strip()
            ho_ten_parts = ho_ten.split()

            try:
                with transaction.atomic():  # Đảm bảo atomic transaction
                    request.user.last_name = ' '.join(ho_ten_parts[:-1]) if len(ho_ten_parts) > 1 else ''
                    request.user.first_name = ho_ten_parts[-1] if ho_ten_parts else ''
                    request.user.email = form.cleaned_data.get('email', '')
                    request.user.save()

                    nguoi_dung.so_dien_thoai = so_dien_thoai
                    nguoi_dung.ho_ten = ho_ten
                    nguoi_dung.email = form.cleaned_data.get('email', '')
                    nguoi_dung.save()

                messages.success(request, 'Cập nhật thông tin thành công!')
                return redirect('chitiet_hoso')

            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra khi cập nhật dữ liệu: {str(e)}')

    else:
        form = SuaHoSoForm(instance=nguoi_dung)

    return render(request, 'nguoidung/sua_hoso.html', {'form': form})

# -------------------- Sua thong tin nguoi dung  ---------------------------
@login_required
@role_required('Quản lý')
def sua_nguoidung(request, user_id):
    user = get_object_or_404(NguoiDung, user_id=user_id)

    if request.method == 'POST':
        form = SuaNguoiDungForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật người dùng thành công!')
            return redirect('quanly_nguoidung')
    else:
        form = SuaNguoiDungForm(instance=user)

    return render(request, 'nguoidung/sua_nguoidung.html', {'form': form})

@login_required
@role_required('Quản lý')
def xoa_nguoidung(request, user_id):
    user = get_object_or_404(User, id=user_id)
    nguoi_dung = user.nguoidung
    if request.method == 'POST':
        try:
            nguoi_dung.delete()
            user.delete()
            messages.success(request, 'Người dùng đã được xóa thành công!')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra khi xóa người dùng: {str(e)}')
        return redirect('quanly_nguoidung')  
    
    return render(request, 'nguoidung/xoa_nguoidung.html', {'user': user})

@login_required
@role_required('Quản lý')
def quanly_dashboard(request):
    # Tổng quan
    total_ho_khau = HoKhau.objects.count()
    total_nhan_khau = NhanKhau.objects.count()
    total_tam_tru = NhanKhau.objects.filter(trang_thai='Tạm trú').count()
    total_tam_vang = NhanKhau.objects.filter(trang_thai='Tạm vắng').count()

    # Dữ liệu biểu đồ
    status_counts = NhanKhau.objects.values('trang_thai').annotate(count=Count('id'))
    chart_data = {
        'labels': [item['trang_thai'] for item in status_counts],
        'data': [item['count'] for item in status_counts],
    }

    # Lọc bảng
    loai_bang = request.GET.get('bang', 'nhankhau')  # 'nhankhau' hoặc 'hokhau'

    # Lọc cho 'nhankhau' (citizens)
    if loai_bang == 'nhankhau':
        query_params = {
            'trang_thai': request.GET.get('trang_thai'),
            'tuoi_min': request.GET.get('tuoi_min'),
            'tuoi_max': request.GET.get('tuoi_max'),
            'nam_den_min': request.GET.get('nam_den_min'),
            'nam_den_max': request.GET.get('nam_den_max')
        }

        queryset = NhanKhau.objects.all()

        # Apply filters for age, status, and date of arrival
        if query_params['trang_thai']:
            queryset = queryset.filter(trang_thai=query_params['trang_thai'])
        if query_params['tuoi_min']:
            min_dob = timezone.now().date() - timezone.timedelta(days=int(query_params['tuoi_min']) * 365)
            queryset = queryset.filter(ngay_sinh__lte=min_dob)
        if query_params['tuoi_max']:
            max_dob = timezone.now().date() - timezone.timedelta(days=int(query_params['tuoi_max']) * 365)
            queryset = queryset.filter(ngay_sinh__gte=max_dob)
        if query_params['nam_den_min']:
            queryset = queryset.filter(thoi_gian_chuyen_den__year__gte=query_params['nam_den_min'])
        if query_params['nam_den_max']:
            queryset = queryset.filter(thoi_gian_chuyen_den__year__lte=query_params['nam_den_max'])

        filtered_nhan_khau = queryset
        filtered_ho_khau = None

    # Lọc cho 'hokhau' (households)
    else:  # bảng hộ khẩu
        query_params = {
            'so_tv_min': request.GET.get('tv_min'),
            'so_tv_max': request.GET.get('tv_max'),
            'dien_tich_min': request.GET.get('dt_min'),
            'dien_tich_max': request.GET.get('dt_max'),
            'toa_nha': request.GET.get('toa_nha'),
            'tang': request.GET.get('tang')
        }

        queryset = HoKhau.objects.all()

        if query_params['so_tv_min']:
            queryset = queryset.filter(tong_thanh_vien__gte=query_params['so_tv_min'])
        if query_params['so_tv_max']:
            queryset = queryset.filter(tong_thanh_vien__lte=query_params['so_tv_max'])
        if query_params['dien_tich_min']:
            queryset = queryset.filter(dien_tich__gte=query_params['dien_tich_min'])
        if query_params['dien_tich_max']:
            queryset = queryset.filter(dien_tich__lte=query_params['dien_tich_max'])
        if query_params['toa_nha']:
            queryset = queryset.filter(toa_nha__icontains=query_params['toa_nha'])
        if query_params['tang']:
            queryset = queryset.filter(tang=query_params['tang'])

        filtered_ho_khau = queryset
        filtered_nhan_khau = None

    return render(request, 'quanly/quanly_dashboard.html', {
        'total_ho_khau': total_ho_khau,
        'total_nhan_khau': total_nhan_khau,
        'total_tam_tru': total_tam_tru,
        'total_tam_vang': total_tam_vang,
        'chart_data': chart_data,
        'bang': loai_bang,
        'filtered_nhan_khau': filtered_nhan_khau,
        'filtered_ho_khau': filtered_ho_khau
    })

@login_required
@role_required('Kế toán')
def ketoan_dashboard(request):
    total_ho_khau = HoKhau.objects.count()  
    total_dong_gop = DongGopPhi.objects.count() 
    total_nhan_khau = NhanKhau.objects.count()

    context = {
        'total_ho_khau': total_ho_khau,
        'total_nhan_khau': total_nhan_khau,
        'total_dong_gop': total_dong_gop,
    }

    return render(request, 'ketoan/ketoan_dashboard.html', context)