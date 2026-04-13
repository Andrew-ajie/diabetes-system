"""
/api/patient/* — JSON API for the mobile uni-app patient client.

All endpoints (except /login) require:
    Authorization: Bearer <token>
"""
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, jsonify, request

from app import db
from app.api_patient import api_patient_bp
from app.models import (
    Consultation,
    ExerciseRecord,
    FamilyMember,
    GlucoseRecord,
    Patient,
    Reminder,
)


# ─── Token helpers ────────────────────────────────────────────────────────────

def _generate_token(patient_id: int) -> str:
    expire_days = current_app.config.get('JWT_EXPIRE_DAYS', 7)
    payload = {
        'patient_id': patient_id,
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=expire_days),
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def _decode_token(token: str):
    return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])


def token_required(f):
    """Decorator: verify Bearer token and inject `current_patient` into kwargs."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': '缺少 Authorization 头'}), 401
        token = auth_header[7:]
        try:
            payload = _decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token 已过期，请重新登录'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token 无效'}), 401
        patient = Patient.query.get(payload.get('patient_id'))
        if not patient:
            return jsonify({'message': '患者不存在'}), 401
        kwargs['current_patient'] = patient
        return f(*args, **kwargs)
    return decorated


def _patient_dict(p: Patient) -> dict:
    return {
        'id': p.id,
        'name': p.name,
        'gender': p.gender,
        'age': p.age,
        'phone': p.phone,
        'address': p.address,
        'diabetes_type': p.diabetes_type,
        'created_at': p.created_at.isoformat() if p.created_at else None,
    }


# ─── Auth ────────────────────────────────────────────────────────────────────

@api_patient_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    phone = (data.get('phone') or '').strip()
    password = data.get('password') or ''

    if not phone or not password:
        return jsonify({'message': '手机号和密码不能为空'}), 400

    patient = Patient.query.filter_by(phone=phone).first()
    if not patient or not patient.check_password(password):
        return jsonify({'message': '手机号或密码错误'}), 401

    token = _generate_token(patient.id)
    return jsonify({'token': token, 'patient': _patient_dict(patient)})


# ─── Patient profile ─────────────────────────────────────────────────────────

@api_patient_bp.route('/me', methods=['GET'])
@token_required
def get_me(current_patient):
    return jsonify(_patient_dict(current_patient))


@api_patient_bp.route('/me', methods=['PUT'])
@token_required
def update_me(current_patient):
    data = request.get_json(silent=True) or {}
    allowed = ('name', 'gender', 'age', 'phone', 'address', 'diabetes_type')
    for field in allowed:
        if field in data:
            setattr(current_patient, field, data[field])
    db.session.commit()
    return jsonify(_patient_dict(current_patient))


# ─── Glucose Records ─────────────────────────────────────────────────────────

@api_patient_bp.route('/glucose', methods=['GET'])
@token_required
def list_glucose(current_patient):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 15, type=int)
    from_str = request.args.get('from')
    to_str = request.args.get('to')

    q = GlucoseRecord.query.filter_by(patient_id=current_patient.id)
    if from_str:
        try:
            q = q.filter(GlucoseRecord.measure_time >= datetime.fromisoformat(from_str))
        except ValueError:
            pass
    if to_str:
        try:
            q = q.filter(GlucoseRecord.measure_time <= datetime.fromisoformat(to_str))
        except ValueError:
            pass
    q = q.order_by(GlucoseRecord.measure_time.desc())
    pagination = q.paginate(page=page, per_page=page_size, error_out=False)
    items = [
        {
            'id': r.id,
            'value': r.value,
            'measure_time': r.measure_time.isoformat(),
            'meal_status': r.meal_status,
            'remark': r.remark,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        }
        for r in pagination.items
    ]
    return jsonify({'items': items, 'total': pagination.total, 'pages': pagination.pages, 'page': page})


@api_patient_bp.route('/glucose', methods=['POST'])
@token_required
def add_glucose(current_patient):
    data = request.get_json(silent=True) or {}
    try:
        value = float(data['value'])
        measure_time = datetime.fromisoformat(data['measure_time'])
    except (KeyError, ValueError, TypeError):
        return jsonify({'message': '参数错误：value 和 measure_time 必填'}), 400

    record = GlucoseRecord(
        patient_id=current_patient.id,
        value=value,
        measure_time=measure_time,
        meal_status=data.get('meal_status') or None,
        remark=(data.get('remark') or '').strip() or None,
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'id': record.id, 'message': '血糖记录已添加'}), 201


@api_patient_bp.route('/glucose/<int:record_id>', methods=['PUT'])
@token_required
def update_glucose(current_patient, record_id):
    record = GlucoseRecord.query.filter_by(id=record_id, patient_id=current_patient.id).first_or_404()
    data = request.get_json(silent=True) or {}
    try:
        if 'value' in data:
            record.value = float(data['value'])
        if 'measure_time' in data:
            record.measure_time = datetime.fromisoformat(data['measure_time'])
    except (ValueError, TypeError):
        return jsonify({'message': '参数错误'}), 400
    if 'meal_status' in data:
        record.meal_status = data['meal_status'] or None
    if 'remark' in data:
        record.remark = (data['remark'] or '').strip() or None
    db.session.commit()
    return jsonify({'message': '血糖记录已更新'})


@api_patient_bp.route('/glucose/<int:record_id>', methods=['DELETE'])
@token_required
def delete_glucose(current_patient, record_id):
    record = GlucoseRecord.query.filter_by(id=record_id, patient_id=current_patient.id).first_or_404()
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '血糖记录已删除'})


# ─── Exercise Records ─────────────────────────────────────────────────────────

@api_patient_bp.route('/exercise', methods=['GET'])
@token_required
def list_exercise(current_patient):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 15, type=int)
    from_str = request.args.get('from')
    to_str = request.args.get('to')

    q = ExerciseRecord.query.filter_by(patient_id=current_patient.id)
    if from_str:
        try:
            q = q.filter(ExerciseRecord.record_time >= datetime.fromisoformat(from_str))
        except ValueError:
            pass
    if to_str:
        try:
            q = q.filter(ExerciseRecord.record_time <= datetime.fromisoformat(to_str))
        except ValueError:
            pass
    q = q.order_by(ExerciseRecord.record_time.desc())
    pagination = q.paginate(page=page, per_page=page_size, error_out=False)
    items = [
        {
            'id': r.id,
            'exercise_type': r.exercise_type,
            'duration': r.duration,
            'calories': r.calories,
            'intensity': r.intensity,
            'record_time': r.record_time.isoformat(),
            'remark': r.remark,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        }
        for r in pagination.items
    ]
    return jsonify({'items': items, 'total': pagination.total, 'pages': pagination.pages, 'page': page})


@api_patient_bp.route('/exercise', methods=['POST'])
@token_required
def add_exercise(current_patient):
    data = request.get_json(silent=True) or {}
    try:
        record_time = datetime.fromisoformat(data['record_time'])
    except (KeyError, ValueError, TypeError):
        return jsonify({'message': '参数错误：record_time 必填'}), 400

    record = ExerciseRecord(
        patient_id=current_patient.id,
        exercise_type=(data.get('exercise_type') or '').strip() or None,
        duration=int(data['duration']) if data.get('duration') else None,
        calories=int(data['calories']) if data.get('calories') else None,
        intensity=data.get('intensity') or None,
        record_time=record_time,
        remark=(data.get('remark') or '').strip() or None,
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'id': record.id, 'message': '运动记录已添加'}), 201


@api_patient_bp.route('/exercise/<int:record_id>', methods=['PUT'])
@token_required
def update_exercise(current_patient, record_id):
    record = ExerciseRecord.query.filter_by(id=record_id, patient_id=current_patient.id).first_or_404()
    data = request.get_json(silent=True) or {}
    try:
        if 'record_time' in data:
            record.record_time = datetime.fromisoformat(data['record_time'])
        if 'duration' in data:
            record.duration = int(data['duration']) if data['duration'] else None
        if 'calories' in data:
            record.calories = int(data['calories']) if data['calories'] else None
    except (ValueError, TypeError):
        return jsonify({'message': '参数错误'}), 400
    if 'exercise_type' in data:
        record.exercise_type = (data['exercise_type'] or '').strip() or None
    if 'intensity' in data:
        record.intensity = data['intensity'] or None
    if 'remark' in data:
        record.remark = (data['remark'] or '').strip() or None
    db.session.commit()
    return jsonify({'message': '运动记录已更新'})


@api_patient_bp.route('/exercise/<int:record_id>', methods=['DELETE'])
@token_required
def delete_exercise(current_patient, record_id):
    record = ExerciseRecord.query.filter_by(id=record_id, patient_id=current_patient.id).first_or_404()
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '运动记录已删除'})


# ─── Reminders ───────────────────────────────────────────────────────────────

@api_patient_bp.route('/reminders', methods=['GET'])
@token_required
def list_reminders(current_patient):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    pagination = (
        Reminder.query
        .filter_by(patient_id=current_patient.id)
        .order_by(Reminder.created_at.desc())
        .paginate(page=page, per_page=page_size, error_out=False)
    )
    items = [
        {
            'id': r.id,
            'content': r.content,
            'level': r.level,
            'created_at': r.created_at.isoformat() if r.created_at else None,
        }
        for r in pagination.items
    ]
    return jsonify({'items': items, 'total': pagination.total, 'pages': pagination.pages, 'page': page})


# ─── Consultation ─────────────────────────────────────────────────────────────

@api_patient_bp.route('/consultation', methods=['GET'])
@token_required
def list_consultation(current_patient):
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 50, type=int)
    pagination = (
        Consultation.query
        .filter_by(patient_id=current_patient.id)
        .order_by(Consultation.created_at.asc())
        .paginate(page=page, per_page=page_size, error_out=False)
    )
    items = [
        {
            'id': m.id,
            'sender': m.sender,
            'content': m.content,
            'created_at': m.created_at.isoformat() if m.created_at else None,
        }
        for m in pagination.items
    ]
    return jsonify({'items': items, 'total': pagination.total, 'pages': pagination.pages, 'page': page})


@api_patient_bp.route('/consultation', methods=['POST'])
@token_required
def send_consultation(current_patient):
    data = request.get_json(silent=True) or {}
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'message': '消息内容不能为空'}), 400
    msg = Consultation(
        patient_id=current_patient.id,
        doctor_id=current_patient.doctor_id,
        sender='patient',
        content=content,
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({'id': msg.id, 'message': '消息已发送'}), 201


# ─── Family Members ───────────────────────────────────────────────────────────

@api_patient_bp.route('/family', methods=['GET'])
@token_required
def list_family(current_patient):
    members = (
        FamilyMember.query
        .filter_by(patient_id=current_patient.id)
        .order_by(FamilyMember.created_at.desc())
        .all()
    )
    items = [
        {
            'id': m.id,
            'name': m.name,
            'relation': m.relation,
            'phone': m.phone,
            'created_at': m.created_at.isoformat() if m.created_at else None,
        }
        for m in members
    ]
    return jsonify({'items': items})


@api_patient_bp.route('/family', methods=['POST'])
@token_required
def add_family(current_patient):
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'message': '家属姓名不能为空'}), 400
    member = FamilyMember(
        patient_id=current_patient.id,
        name=name,
        relation=(data.get('relation') or '').strip() or None,
        phone=(data.get('phone') or '').strip() or None,
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({'id': member.id, 'message': f'家属「{name}」已添加'}), 201


@api_patient_bp.route('/family/<int:member_id>', methods=['DELETE'])
@token_required
def delete_family(current_patient, member_id):
    member = FamilyMember.query.filter_by(id=member_id, patient_id=current_patient.id).first_or_404()
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': '家属信息已删除'})


# ─── Statistics ──────────────────────────────────────────────────────────────

@api_patient_bp.route('/stats/glucose', methods=['GET'])
@token_required
def stats_glucose(current_patient):
    range_param = request.args.get('range', 'week')
    days = 30 if range_param == 'month' else 7
    since = datetime.now(tz=timezone.utc) - timedelta(days=days)

    records = (
        GlucoseRecord.query
        .filter(
            GlucoseRecord.patient_id == current_patient.id,
            GlucoseRecord.measure_time >= since,
        )
        .order_by(GlucoseRecord.measure_time.asc())
        .all()
    )

    # Group by date
    by_date: dict = {}
    for r in records:
        date_str = r.measure_time.strftime('%m-%d')
        by_date.setdefault(date_str, []).append(r.value)

    labels = list(by_date.keys())
    averages = [round(sum(v) / len(v), 1) for v in by_date.values()]
    all_values = [r.value for r in records]

    return jsonify({
        'labels': labels,
        'averages': averages,
        'avg': round(sum(all_values) / len(all_values), 1) if all_values else None,
        'max': max(all_values) if all_values else None,
        'min': min(all_values) if all_values else None,
        'count': len(records),
    })


@api_patient_bp.route('/stats/exercise', methods=['GET'])
@token_required
def stats_exercise(current_patient):
    range_param = request.args.get('range', 'week')
    days = 30 if range_param == 'month' else 7
    since = datetime.now(tz=timezone.utc) - timedelta(days=days)

    records = (
        ExerciseRecord.query
        .filter(
            ExerciseRecord.patient_id == current_patient.id,
            ExerciseRecord.record_time >= since,
        )
        .order_by(ExerciseRecord.record_time.asc())
        .all()
    )

    by_date: dict = {}
    for r in records:
        date_str = r.record_time.strftime('%m-%d')
        entry = by_date.setdefault(date_str, {'duration': 0, 'calories': 0})
        entry['duration'] += r.duration or 0
        entry['calories'] += r.calories or 0

    labels = list(by_date.keys())
    durations = [v['duration'] for v in by_date.values()]
    calories = [v['calories'] for v in by_date.values()]

    return jsonify({
        'labels': labels,
        'durations': durations,
        'calories': calories,
        'total_duration': sum(r.duration or 0 for r in records),
        'total_calories': sum(r.calories or 0 for r in records),
        'count': len(records),
    })
