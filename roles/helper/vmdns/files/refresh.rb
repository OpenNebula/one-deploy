#!/usr/bin/env ruby
# managed by one-deploy

RFC1123_REGEX = %r{ \A

                    (?=.{1,253}\z)

                    (?:
                        [a-zA-Z0-9]
                        (?:
                            [a-zA-Z0-9-]{0,61}
                            [a-zA-Z0-9]
                        )?
                        [.]
                    )*

                    [a-zA-Z0-9]
                    (?:
                        [a-zA-Z0-9-]{0,61}
                        [a-zA-Z0-9]
                    )?

                    \z }x

def run(cmd)
    o = `#{cmd}`
    s = $?
    raise unless s.success?
    o
end

def throttle(thrt_lock = '/var/tmp/vmdns-thrt.lock',
             exec_lock = '/var/tmp/vmdns-exec.lock')
    # Silently drop rapid bursts.
    File.open(thrt_lock, File::CREAT | File::RDWR, 0o0644) do |lf|
        return unless lf.flock(File::LOCK_EX | File::LOCK_NB)
        sleep(1)
    end
    # Ensure exclusive execution.
    File.open(exec_lock, File::CREAT | File::RDWR, 0o0644) do |lf|
        lf.flock(File::LOCK_EX)
        yield
    end
end

def refresh(hosts_file = '/etc/hosts')
    require 'json'

    document = JSON.parse run('onevm list --json')

    File.open(hosts_file, File::RDONLY) do |hf|
        hf.each_line(chomp: true).each_with_object({block: false, lines: []}) do |line, acc|
            case line
            when '# BEGIN VMDNS (one-deploy)'
                acc[:block] = true
            when '# END VMDNS (one-deploy)'
                acc[:block] = false
            else
                acc[:lines] << line unless acc[:block]
            end
        end[:lines]
    end.then do |unmanaged|
        document.dig('VM_POOL', 'VM').to_a.each_with_object([]) do |vm, acc|
            ip = [vm.dig('TEMPLATE', 'NIC')].flatten.dig(0, 'IP')
            next unless ip

            name = vm['NAME']
            next unless name && name =~ RFC1123_REGEX

            id = vm['ID']
            next unless id

            acc << "#{ip} #{name} one-#{id}"
        end.then do |managed|
            File.open(hosts_file, File::CREAT | File::RDWR, 0o0644) do |hf|
                hf.rewind

                unmanaged.each { |line| hf.puts(line) }

                # NOTE: The original / unmanaged data is never completely removed
                #       from the file.
                hf.truncate(hf.pos)

                unless managed.empty?
                    hf.puts('# BEGIN VMDNS (one-deploy)')

                    managed.each { |line| hf.puts(line) }

                    hf.puts('# END VMDNS (one-deploy)')
                end
            end
        end
    end
end

throttle { refresh } if [nil, 'leader'].include?(ARGV[0])
