import 'package:flutter/material.dart';

import 'models/uye.dart';
import 'services/uye_api_service.dart';

void main() {
  runApp(const SporSalonuApp());
}

class SporSalonuApp extends StatelessWidget {
  const SporSalonuApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Spor Salonu Yönetim Sistemi',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const UyeListesiSayfasi(),
    );
  }
}

class UyeListesiSayfasi extends StatefulWidget {
  const UyeListesiSayfasi({super.key});

  @override
  State<UyeListesiSayfasi> createState() => _UyeListesiSayfasiState();
}

class _UyeListesiSayfasiState extends State<UyeListesiSayfasi> {
  final UyeApiService _uyeApiService = UyeApiService();

  late Future<List<Uye>> _uyelerFuture;

  @override
  void initState() {
    super.initState();
    _uyelerFuture = _uyeApiService.uyeleriGetir();
  }

  Future<void> _yenile() async {
    setState(() {
      _uyelerFuture = _uyeApiService.uyeleriGetir();
    });
  }

  String _tarihKisalt(String? tarih) {
    if (tarih == null || tarih.isEmpty) {
      return '';
    }

    if (tarih.length >= 10) {
      return tarih.substring(0, 10);
    }

    return tarih;
  }

  Future<void> _uyeFormDialogAc({Uye? mevcutUye}) async {
    final formKey = GlobalKey<FormState>();

    final adController = TextEditingController(text: mevcutUye?.ad ?? '');
    final soyadController = TextEditingController(text: mevcutUye?.soyad ?? '');
    final telefonController =
        TextEditingController(text: mevcutUye?.telefon ?? '');
    final emailController = TextEditingController(text: mevcutUye?.email ?? '');
    final dogumTarihiController = TextEditingController(
      text: _tarihKisalt(mevcutUye?.dogumTarihi),
    );

    String secilenCinsiyet = mevcutUye?.cinsiyet ?? 'Erkek';
    bool aktifMi = mevcutUye?.aktifMi ?? true;
    bool kaydediliyor = false;

    final guncellemeMi = mevcutUye != null;

    await showDialog(
      context: context,
      builder: (dialogContext) {
        return StatefulBuilder(
          builder: (dialogContext, setDialogState) {
            return AlertDialog(
              title: Text(guncellemeMi ? 'Üye Güncelle' : 'Yeni Üye Ekle'),
              content: SizedBox(
                width: 420,
                child: Form(
                  key: formKey,
                  child: SingleChildScrollView(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        TextFormField(
                          controller: adController,
                          decoration: const InputDecoration(
                            labelText: 'Ad',
                            border: OutlineInputBorder(),
                          ),
                          validator: (value) {
                            if (value == null || value.trim().length < 2) {
                              return 'Ad en az 2 karakter olmalıdır.';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: soyadController,
                          decoration: const InputDecoration(
                            labelText: 'Soyad',
                            border: OutlineInputBorder(),
                          ),
                          validator: (value) {
                            if (value == null || value.trim().length < 2) {
                              return 'Soyad en az 2 karakter olmalıdır.';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: telefonController,
                          decoration: const InputDecoration(
                            labelText: 'Telefon',
                            hintText: '05550000000',
                            border: OutlineInputBorder(),
                          ),
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return 'Telefon boş bırakılamaz.';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: emailController,
                          decoration: const InputDecoration(
                            labelText: 'E-posta',
                            hintText: 'ornek@mail.com',
                            border: OutlineInputBorder(),
                          ),
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return 'E-posta boş bırakılamaz.';
                            }
                            if (!value.contains('@')) {
                              return 'Geçerli bir e-posta giriniz.';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 12),
                        DropdownButtonFormField<String>(
                          initialValue: secilenCinsiyet,
                          decoration: const InputDecoration(
                            labelText: 'Cinsiyet',
                            border: OutlineInputBorder(),
                          ),
                          items: const [
                            DropdownMenuItem(
                              value: 'Erkek',
                              child: Text('Erkek'),
                            ),
                            DropdownMenuItem(
                              value: 'Kadın',
                              child: Text('Kadın'),
                            ),
                            DropdownMenuItem(
                              value: 'Belirtmek İstemiyor',
                              child: Text('Belirtmek İstemiyor'),
                            ),
                          ],
                          onChanged: (value) {
                            if (value != null) {
                              setDialogState(() {
                                secilenCinsiyet = value;
                              });
                            }
                          },
                        ),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: dogumTarihiController,
                          decoration: const InputDecoration(
                            labelText: 'Doğum Tarihi',
                            hintText: '2000-01-01',
                            border: OutlineInputBorder(),
                          ),
                          validator: (value) {
                            if (value == null || value.trim().isEmpty) {
                              return 'Doğum tarihi boş bırakılamaz.';
                            }
                            return null;
                          },
                        ),
                        if (guncellemeMi) ...[
                          const SizedBox(height: 12),
                          SwitchListTile(
                            title: const Text('Aktif Üye'),
                            value: aktifMi,
                            onChanged: (value) {
                              setDialogState(() {
                                aktifMi = value;
                              });
                            },
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),
              actions: [
                TextButton(
                  onPressed: kaydediliyor
                      ? null
                      : () {
                          Navigator.of(dialogContext).pop();
                        },
                  child: const Text('İptal'),
                ),
                ElevatedButton.icon(
                  onPressed: kaydediliyor
                      ? null
                      : () async {
                          if (!formKey.currentState!.validate()) {
                            return;
                          }

                          setDialogState(() {
                            kaydediliyor = true;
                          });

                          try {
                            if (guncellemeMi) {
                              await _uyeApiService.uyeGuncelle(
                                uyeId: mevcutUye.uyeId,
                                ad: adController.text.trim(),
                                soyad: soyadController.text.trim(),
                                telefon: telefonController.text.trim(),
                                email: emailController.text.trim(),
                                cinsiyet: secilenCinsiyet,
                                dogumTarihi:
                                    dogumTarihiController.text.trim(),
                                aktifMi: aktifMi,
                              );
                            } else {
                              await _uyeApiService.uyeEkle(
                                ad: adController.text.trim(),
                                soyad: soyadController.text.trim(),
                                telefon: telefonController.text.trim(),
                                email: emailController.text.trim(),
                                cinsiyet: secilenCinsiyet,
                                dogumTarihi:
                                    dogumTarihiController.text.trim(),
                              );
                            }

                            if (!mounted) return;

                            if (dialogContext.mounted) {
                              Navigator.of(dialogContext).pop();
                            }

                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(
                                  guncellemeMi
                                      ? 'Üye başarıyla güncellendi.'
                                      : 'Üye başarıyla eklendi.',
                                ),
                              ),
                            );

                            await _yenile();
                          } catch (e) {
                            setDialogState(() {
                              kaydediliyor = false;
                            });

                            if (!mounted) return;

                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(
                                  guncellemeMi
                                      ? 'Üye güncellenemedi: $e'
                                      : 'Üye eklenemedi: $e',
                                ),
                              ),
                            );
                          }
                        },
                  icon: kaydediliyor
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : Icon(guncellemeMi ? Icons.edit : Icons.save),
                  label: Text(
                    kaydediliyor
                        ? 'Kaydediliyor'
                        : guncellemeMi
                            ? 'Güncelle'
                            : 'Kaydet',
                  ),
                ),
              ],
            );
          },
        );
      },
    );
  }

  Future<void> _uyeSilOnayla(Uye uye) async {
    final onay = await showDialog<bool>(
      context: context,
      builder: (dialogContext) {
        return AlertDialog(
          title: const Text('Üye Sil'),
          content: Text(
            '${uye.ad} ${uye.soyad} adlı üyeyi silmek istediğine emin misin?',
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(dialogContext).pop(false);
              },
              child: const Text('Vazgeç'),
            ),
            ElevatedButton.icon(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
              ),
              onPressed: () {
                Navigator.of(dialogContext).pop(true);
              },
              icon: const Icon(Icons.delete),
              label: const Text('Sil'),
            ),
          ],
        );
      },
    );

    if (onay != true) {
      return;
    }

    try {
      await _uyeApiService.uyeSil(uye.uyeId);

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Üye başarıyla silindi.'),
        ),
      );

      await _yenile();
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Üye silinemedi: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F6FA),
      appBar: AppBar(
        title: const Text('Spor Salonu Yönetim Sistemi'),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _uyeFormDialogAc(),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
        icon: const Icon(Icons.person_add),
        label: const Text('Üye Ekle'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: FutureBuilder<List<Uye>>(
          future: _uyelerFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }

            if (snapshot.hasError) {
              return Center(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Text(
                      'Üyeler yüklenirken hata oluştu:\n${snapshot.error}',
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              );
            }

            final uyeler = snapshot.data ?? [];

            if (uyeler.isEmpty) {
              return const Center(
                child: Text('Kayıtlı üye bulunamadı.'),
              );
            }

            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _OzetKart(
                  aktifUyeSayisi: uyeler.where((u) => u.aktifMi).length,
                  toplamUyeSayisi: uyeler.length,
                ),
                const SizedBox(height: 16),
                const Text(
                  'Üye Listesi',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                Expanded(
                  child: RefreshIndicator(
                    onRefresh: _yenile,
                    child: ListView.builder(
                      itemCount: uyeler.length,
                      itemBuilder: (context, index) {
                        final uye = uyeler[index];

                        return Card(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundColor: Colors.deepPurple,
                              foregroundColor: Colors.white,
                              child: Text(uye.ad[0].toUpperCase()),
                            ),
                            title: Text(
                              '${uye.ad} ${uye.soyad}',
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            subtitle: Text(
                              'Telefon: ${uye.telefon}\nE-posta: ${uye.email ?? "-"}',
                            ),
                            trailing: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Chip(
                                  label: Text(uye.aktifMi ? 'Aktif' : 'Pasif'),
                                  backgroundColor: uye.aktifMi
                                      ? Colors.green.shade100
                                      : Colors.red.shade100,
                                ),
                                IconButton(
                                  tooltip: 'Üyeyi Güncelle',
                                  icon: const Icon(
                                    Icons.edit,
                                    color: Colors.blue,
                                  ),
                                  onPressed: () {
                                    _uyeFormDialogAc(mevcutUye: uye);
                                  },
                                ),
                                IconButton(
                                  tooltip: 'Üyeyi Sil',
                                  icon: const Icon(
                                    Icons.delete,
                                    color: Colors.red,
                                  ),
                                  onPressed: () {
                                    _uyeSilOnayla(uye);
                                  },
                                ),
                              ],
                            ),
                            isThreeLine: true,
                          ),
                        );
                      },
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _OzetKart extends StatelessWidget {
  final int aktifUyeSayisi;
  final int toplamUyeSayisi;

  const _OzetKart({
    required this.aktifUyeSayisi,
    required this.toplamUyeSayisi,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.deepPurple,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            const Icon(
              Icons.fitness_center,
              color: Colors.white,
              size: 42,
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                'Toplam Üye: $toplamUyeSayisi\nAktif Üye: $aktifUyeSayisi',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  height: 1.5,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}