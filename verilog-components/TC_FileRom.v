module TC_FileRom (clk, rst, en, address, out);
    parameter BIT_WIDTH = 65536;
    parameter rom = "test_jumps.mem";
    input clk;
    input rst;
    input en;
    input [15:0] address;
    output reg [63:0] out;

    reg [7:0] mem [BIT_WIDTH:0];
    integer fid;
    integer fBIT_WIDTH;
    integer data;

    initial begin
        //$readmemh(rom, mem);
        fid = $fopen(rom, "rb");
        if (fid == 0) begin
            $display("cannot open file");
            $stop;
        end
        fBIT_WIDTH = $fseek(fid, 0, 2);
        if (fBIT_WIDTH == -1) begin
            $display("cannot move file pointer");
            $stop;
        end
        fBIT_WIDTH = $ftell(fid);
        $display("file is %0d bytes", fBIT_WIDTH); 
        $fseek(fid, 0, 0);
        data = $fread(fid, mem[0]);
        $display("read %0d vectors\n", data);
        //data = $fcloser(fid);
        
        $fclose(fid);
    end

    always @ (posedge clk or posedge rst) begin
        if (rst) begin
            out <= {64{1'b0}};
        end else if (!en) begin
            out <= {64{1'b0}};
        end else if (address == 16'b1111_1111_1111_1111) begin
            out <= 0;
        end else begin
            out[7:0] <= mem[address];
            out[15:8] <= mem[address+1];
            out[23:16] <= mem[address+2];
            out[31:24] <= mem[address+3];
            out[39:32] <= mem[address+4];
            out[47:40] <= mem[address+5];
            out[55:48] <= mem[address+6];
            out[63:56] <= mem[address+7];
        end
    end
endmodule

